import os
from jbrowse_jupyter.util import is_URL,defaults, guess_file_name, get_name
from jbrowse_jupyter.tracks import guess_adapter_type, guess_track_type, check_track_data, get_from_config_adapter

def create(viewType, **kwargs):
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
        # TODO: add converter.py call here
        raise TypeError("currently not supporting JB2 configs files")
    elif viewType == "config":
        if "conf" in kwargs:
            # config from an object
            conf=kwargs["conf"]
        else:
            # default empty configuration object
            return JBrowseConfig()
    else:
        raise TypeError(f'Invalid view type {viewType}, please chose from "view" or "config"')
    return JBrowseConfig(conf=conf)
class JBrowseConfig:
    def __init__(self, conf=None):
        # TODO make sure if a conf is passed, that is mapped to all the defaults
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
            "configuration": {}
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
    def set_assembly(self, assembly_data, aliases, refname_aliases):
        if (is_URL(assembly_data)):
            # get name
            name = get_name(assembly_data)
            assembly_adapter = guess_adapter_type(assembly_data, 'uri')
            assembly_config = {
                "name": name,
                "sequence": {
                    "type": "ReferenceSequenceTrack",
                    "trackId": f'{name}-ReferenceSequenceTrack',
                    "adapter": assembly_adapter
                },
                "aliases": aliases,
                "refNameAliases": refname_aliases,
            }
            self.config["assembly"] = assembly_config
        else:
            raise TypeError("Local files are not currently supported.") 

    # ============ Tracks =============

    def get_reference_track(self):
        """
        Returns the reference track for a default session
        """
        assembly_name = self.get_assembly_name()
        configuration = assembly_name + "-ReferenceSequenceTrack"
        return {
            "type": "ReferenceSequenceTrack",
            "configuration": configuration,
            "displays": [
                {
                    "type": "LinearBasicDisplay",
                    "configuration": configuration + "-LinearBasicDisplay"
                }
            ],
        }

    def get_tracks(self):
        # TODO: add param here to specify which tracks we want to get
        # such as feature, alignments, variant, or wiggle
        """returns list of tracks in the configuration"""
        return self.config["tracks"]

    def add_df_track(self, track_data, name, **kwargs):
        # TODO: implement it
        """
        Adds a track from a data frame

        :param df: the data frame with track data. Must have cols 
            refName, start, end, name. The column additional can optionally be 
            include with more feature information. If a score column is 
            present, it will be used and the track will be rendered to display 
            quantitative features.
        :param str name: name for the track
        """
        overwrite = kwargs.get('overwrite', False)
        # check that the required columns are present
        check_track_data(track_data)
        # if score column is present => QuantitativeTrack, else FeatureTrack
        if not self.get_assembly():
            raise Exception("Please set the assembly before adding a track.")
        assembly_name = self.get_assembly_name()
        trackId = f'{assembly_name}-{name}'
        trackType = "FeatureTrack"
        if "score" in track_data:
            trackType = "QuantitativeTrack"
        adapter = get_from_config_adapter(track_data)
        print('from config', adapter)
        # check that the trackId does not exist yet
        if trackId in self.tracks_ids_map and not overwrite:
            # print("hello")
            raise TypeError(f'track with trackId: "{trackId}" already exists in config. Set overwrite to True if you want to overwrite it.')
        elif trackId in self.tracks_ids_map and overwrite:
            # delete track and overwrite it
            oldTracks = self.get_tracks()
            self.config["tracks"] = [track for track in oldTracks if track["trackId"] != trackId]
        else:
            self.tracks_ids_map.add(name)
        df_track_config = {
            "type": trackType,
            "trackId": trackId,
            "name": name,
            "assemblyNames": [assembly_name],
            "adapter": adapter
        }
        print("=====================")
        print('conf ', df_track_config)
        newTracks = self.get_tracks()
        newTracks.append(df_track_config)
        self.config["tracks"] = newTracks
        

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
        if not data:
            raise TypeError("A path to the track data is required. None was provided.")
        local = kwargs.get('local', False) 
        name = kwargs.get('name', None) 
        index = kwargs.get('index', None)
        overwrite = kwargs.get('overwrite', False)
        # check that the assembly is configured
        if not self.get_assembly():
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
            # print("ADAPTER", adapter)
            # Error if adapter is unknown or unsupported
            if (adapter["type"] == "UNKNOWN"): 
                raise TypeError("Adapter type is not recognized")
            if (adapter["type"] == "UNSUPPORTED"): 
                raise TypeError("Adapter type is not supported")

            if adapter["type"] == "CramAdapter":
                # get sequence adapter
                extra_config = self.get_assembly()["sequence"]["adapter"]
                adapter["sequenceAdapter"] = extra_config
                # print("NEW ADAPTER", adapter)
            # ==== set up track information =========
            trackType = guess_track_type(adapter["type"])
            # print("============== type: ", trackType)
            if trackType not in {'AlignmentsTrack', 'QuantitativeTrack', 'VariantTrack', 'FeatureTrack', 'ReferenceSequenceTrack'}:
                raise TypeError("Track type is not supported")
            # uses filename as trackId
            trackId = guess_file_name(data)
            trackName = trackId if name is None else name

            # print("======\n")
            # print("tracks", self.get_tracks())
            if trackId in self.tracks_ids_map and not overwrite:
                # print("hello")
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
    # def set_default_session(self, assembly, displayed_tracks, display_assembly=True):
    #     reference_track = self.get_reference_track(assembly)
    #     #tracks = self.get_tracks(assembly, displayed_tracks, display_assembly)
    #     self.config["defaultSession"] = {
    #         "name": "my session",
    #         "view": {
    #             "id": "LinearGenomeView",
    #             "type": "LinearGenomeView",
    #             "tracks": [reference_track]
    #         }
    #     }

    # ====== theme ===============
    def set_theme(self,primary, secondary=None, tertiary=None, quaternary=None):
        palette = {
           "primary": {
                "main": primary
            } 
        }
        if secondary:
            palette["secondary"] = {
                "main": secondary
            }
        if tertiary:
            palette["tertiary"] = {
                "main": tertiary
            }
        if quaternary:
            palette["quaternary"] = {
                "main": quaternary
            }
        self.config["configuration"] = {
            "theme": {
                "palette": palette
            }
        }
