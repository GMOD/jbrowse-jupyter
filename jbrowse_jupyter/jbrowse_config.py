from jbrowse_jupyter.util import is_URL,defaults
from jbrowse_jupyter.tracks import guess_adapter_type, guess_track_type, guess_track_name

def create_jbrowse2(viewType, **kwargs):
    # TODO: maybe add aliases of hg19 and hg38
    available_genomes = {"hg19", "hg38"}
    conf = {}
    if viewType == "view":
        if "genome" in kwargs:
            genome = kwargs["genome"]
            if genome in available_genomes:
                conf = defaults(genome)
            else:
                raise NameError(genome, "is not a valid default genome to view")
        else:
            raise TypeError("genome is required arg for viewType=view")
    elif viewType == "JB2config":
        # if "path" in kwargs:
        #     # TODO call parser
        # else:
        #     raise TypeError("path is required arg for viewType=JB2config")
        raise TypeError("currently not supporting JB2 web configs to React JBrowse LGV")
    elif viewType == "config":
        if "conf" in kwargs:
            # config from an object
            conf=kwargs["conf"]
        else:
            # default empty configuration object
            return JBrowseConfig()
    else:
        raise TypeError(f'Invalid view type {viewType}, please chose from "view", "JB2config", or "config"')
    return JBrowseConfig(conf=conf)
class JBrowseConfig:
    def __init__(self, conf=None):
        self.config = {
            "assembly": {},
            "tracks": [],
            "defaultSession": {
                "name": "default-session",
                "view": {
                    "id": 'linearGenomeView',
                    "type": 'LinearGenomeView',
                    "tracks":[]
                }
            },
            "location": "",
        } if conf is None else conf
        self.tracks_ids_map = set()

    def get_config(self):
        return self.config
    
    # ========== Assembly ===========

    def get_assembly(self):
        return self.config["assembly"]
    
    def get_assembly_name(self):
        if self.get_assembly():
            return self.get_assembly()["name"]
        else:
            raise Exception("Can not get assembly name. Please configure the assembly first.")

    # TODO infer the type of the adapter based on file name
    # TODO infer name of the assembly based on the file name
    # TODO check if the assembly data is a url
    def set_assembly(self, assembly_data, aliases, refname_aliases, bgzip=False):
        if not bgzip:
            self.unzipped_assembly(assembly_data, aliases, refname_aliases)
        else:
            self.zipped_assembly(assembly_data, aliases, refname_aliases)

    def unzipped_assembly(self, assembly_data, aliases=[], refname_aliases=[]):
        name = self.get_name(assembly_data)

        self.config["assembly"] = {
            "name": name,
            "sequence": {
                "type": "ReferenceSequenceTrack",
                "trackId": name + "-ReferenceSequenceTrack",
                "adapter": {
                    "type": "BgzipFastaAdapter",
                    "fastaLocation": {
                        "uri": assembly_data,
                    },
                    "faiLocation": {
                        "uri": assembly_data + ".fai",
                    },
                },
            },
            "aliases": aliases,
            "refNameAliases": refname_aliases,
        }

    def zipped_assembly(self, assembly_data, aliases, refname_aliases):
        name = self.get_name(assembly_data)
        self.config["assembly"] = {
            "name": name,
            "sequence": {
                "type": "ReferenceSequenceTrack",
                "trackId": name + "-ReferenceSequenceTrack",
                "adapter": {
                    "type": "BgzipFastaAdapter",
                    "fastaLocation": {
                        "uri": assembly_data,
                    },
                    "faiLocation": {
                        "uri": assembly_data + ".fai",
                    },
                    "gziLocation": {
                        "uri": assembly_data + ".gzi",
                    },
                },
            },
            "aliases": aliases,
            "refNameAliases": refname_aliases,
        }

    def get_name(self, assembly_file):
        name_end = 0
        name_start = 0
        for i in range(0, len(assembly_file)):
            if (
                assembly_file[len(assembly_file) - i - 1 : len(assembly_file) - i]
                == "/"
            ):
                name_start = len(assembly_file) - i
                break
        for i in range(name_start, len(assembly_file)):
            if assembly_file[i : i + 1] == ".":
                name_end = i
                break

        return assembly_file[name_start:name_end]

    # ============ Tracks =============

    def get_reference_track(self, assembly, display_assembly):
        # TODO: what is the config assembly, same as param?
        assembly_name = self.config[assembly]["name"]
        configuration = assembly_name + "-ReferenceSequenceTrack"
        ref = {}
        if display_assembly:
            ref = {
                "type": "ReferenceSequenceTrack",
                "configuration": configuration,
                "displays": [
                    {
                        "type": "LinearBasicDisplay",
                        "configuration": configuration + "-LinearBasicDisplay"
                    }
                ],

            }
        return 

    def get_tracks(self):
        """returns list of tracks in the configuration"""
        return self.config["tracks"]

    def add_track(self, data, **kwargs):
        """
        Adds a track subconfiguration to the list of tracks
        in the config.

        :param str data: Track file or URL (currently only supporting URL)
        :param str name: Optional name for the track (defaults to data filename)
        :param str index: Optional index file for the track (default None)
        :param boolean local: is the track data a local file (default False)
        :param boolean overwrite: Overwrites existing track if it exists in 
            list of tracks (default False)
        :raises TypeError: if track type is not supported
        """
        local = kwargs.get('local', False) 
        name = kwargs.get('name', None) 
        index = kwargs.get('index', None)
        overwrite = kwargs.get('overwrite', False)
        # check that the assembly is configured
        if not self.get_assembly:
            raise Exception("Please set the assembly before adding a track.")
        assemblyNames = [self.get_assembly_name()]
        
        # TODO: local file support for track data and track index using local files
        # useIndex = is_URL(index) if index is not None else False
        # argsTrack = location = path/data
        # TODO: get effective and working locations for track data and track index when
        # local file support is added
        if is_URL(data):
            # we are defaulting to uri protocol since we have not added local file support
            adapter = guess_adapter_type(data, 'uri', "defaultIndex")
            print("ADAPTER", adapter)
            # Error if adapter is unknown or unsupported
            if (adapter["type"] == "UNKNOWN"): 
                raise TypeError("Track type is not recognized")
            if (adapter["type"] == "UNSUPPORTED"): 
                raise TypeError("Track type is not supported")

            # ==== set up track information =========
            trackType = guess_track_type(adapter["type"])
            # uses filename as trackId
            trackId = guess_track_name(data)
            trackName = trackId if name is None else name

            # print("======\n")
            # print("tracks", self.get_tracks())
            if trackId in self.tracks_ids_map and not overwrite:
                print("hello")
                raise TypeError(f'track with trackId: "{trackId}" already exists in config, set overwrite to True if you want to overwrite it.')
            elif trackId in self.tracks_ids_map and overwrite:
                # delete track and overwrite it
                oldTracks = self.get_tracks()
                self.config["tracks"] = [track for track in oldTracks if track["trackId"] != trackId]
            else:
                self.tracks_ids_map.add(trackName)
            
            # print('===== Debugging ======\n')
            # print(f'Name is: {trackName}')
            # print(f'Type is: {trackType}')
            # print(f'TrackId is: {trackId}')
            # print(f'Assembly name(s) is: {assemblyNames}')
            track_config = {
                "type": trackType,
                "trackId": trackId,
                "name": trackName,
                "assemblyNames": assemblyNames,
                "adapter": adapter
            }
            newTracks = self.get_tracks()
            newTracks.append(track_config)
            self.config["tracks"] = newTracks       
        else:
            raise TypeError("Local files are not currently supported.")

    # ======= location ===========  
    def set_location(self, location):
        """ returns location subconfiguration"""
        self.config["location"] = location


    # ======= default session ========
    def set_default_session(self, assembly, displayed_tracks, display_assembly=True):
        reference_track = self.get_reference_track(assembly, display_assembly)
        #tracks = self.get_tracks(assembly, displayed_tracks, display_assembly)
        self.config["defaultSession"] = {
            "name": "my session",
            "view": {
                "id": "LinearGenomeView",
                "type": "LinearGenomeView",
                "tracks": reference_track
            }
        }
