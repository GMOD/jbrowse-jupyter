import os
from jbrowse_jupyter.util import is_URL,defaults, guess_file_name, get_name
from jbrowse_jupyter.tracks import guess_adapter_type, guess_track_type, check_track_data, get_from_config_adapter, guess_display_type

def create(viewType, **kwargs):
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
            "aggregateTextSearchAdapters": [],
            "location": "",
            "configuration": {}
        } if conf is None else conf
        if conf is not None:
            ids = {x["trackId"]: x for x in conf["tracks"]}
            self.tracks_ids_map = ids
        self.tracks_ids_map = {}
        # print("trackIds map", self.tracks_ids_map.keys())

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

    # TODO: test two bit adapter and other supported assembly types
    def set_assembly(self, assembly_data, aliases, refname_aliases):
        if (is_URL(assembly_data)):
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
        configuration = f'{assembly_name}-ReferenceSequenceTrack'
        return {
            "type": "ReferenceSequenceTrack",
            "configuration": configuration,
            "displays": [
                {
                    "type": "LinearReferenceSequenceDisplay",
                    "configuration": f'{configuration}-LinearReferenceSequenceDisplay',
                }
            ],
        }

    def get_track_display(self, track):
        track_type = track["type"]
        track_id = track["trackId"]
        display_type = guess_display_type(track_type)
        return {
            "type": track_type,
            "configuration": track_id,
            "displays": [
                {
                    "type": display_type,
                    "configuration": f'{track_id}-{display_type}'
                }
            ]
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
            refName, start, end, name. The refName and name column values must
            be strings while the start and end must be integers.
            The column additional can optionally be include with more feature information.
            If a score column is present, it will be used and the track will be rendered 
            to display quantitative features. Scores must also be integers.
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
        df_track_config = {
            "type": trackType,
            "trackId": trackId,
            "name": name,
            "assemblyNames": [assembly_name],
            "adapter": adapter
        }
        # check that the trackId does not exist yet
        if trackId in self.tracks_ids_map.keys() and not overwrite:
            # print("hello")
            raise TypeError(f'track with trackId: "{trackId}" already exists in config. Set overwrite to True if you want to overwrite it.')
        if trackId in self.tracks_ids_map.keys() and overwrite:
            # delete track and overwrite it
            oldTracks = self.get_tracks()
            self.config["tracks"] = [track for track in oldTracks if track["trackId"] != trackId]
       
        newTracks = self.get_tracks()
        newTracks.append(df_track_config)
        self.config["tracks"] = newTracks
        self.tracks_ids_map[trackId] = df_track_config

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
            if (adapter["type"] == "UNKNOWN"): 
                raise TypeError("Adapter type is not recognized")
            if (adapter["type"] == "UNSUPPORTED"): 
                raise TypeError("Adapter type is not supported")

            if adapter["type"] == "CramAdapter":
                # get sequence adapter
                extra_config = self.get_assembly()["sequence"]["adapter"]
                adapter["sequenceAdapter"] = extra_config
            trackType = guess_track_type(adapter["type"])
            if trackType not in {'AlignmentsTrack', 'QuantitativeTrack', 'VariantTrack', 'FeatureTrack', 'ReferenceSequenceTrack'}:
                raise TypeError("Track type is not supported")
            # uses filename as trackId
            trackId = guess_file_name(data)
            trackName = trackId if name is None else name
            track_config = {
                "type": trackType,
                "trackId": trackId,
                "name": trackName,
                "assemblyNames": assemblyNames,
                "adapter": adapter
            }
            # print("======\n")
            # print("tracks", self.get_tracks())
            if trackId in self.tracks_ids_map.keys() and not overwrite:
                # print("hello")
                raise TypeError(f'track with trackId: "{trackId}" already exists in config, set overwrite to True if you want to overwrite it.')
            if trackId in self.tracks_ids_map.keys() and overwrite:
                # delete track and overwrite it
                oldTracks = self.get_tracks()
                self.config["tracks"] = [track for track in oldTracks if track["trackId"] != trackId]
            
            # print('===== Debugging ======\n')
            # print(f'Name is: {trackName}')
            # print(f'Type is: {trackType}')
            # print(f'TrackId is: {trackId}')
            # print(f'Assembly name(s) is: {assemblyNames}')

            newTracks = self.get_tracks()
            newTracks.append(track_config)
            self.config["tracks"] = newTracks
            self.tracks_ids_map[trackId] = track_config       
        else:
            raise TypeError("Local files are not currently supported.")

    # ======= location ===========  
    def set_location(self, location):
        """ returns location subconfiguration"""
        self.config["location"] = location


    # ======= default session ========
    def set_default_session(self,displayed_tracks,display_assembly=True):
        reference_track = {}
        tracks_configs = []
        if (display_assembly):
            reference_track = self.get_reference_track()
            tracks_configs.append(reference_track)
        
        # make sure all displayed_track names
        # print(self.tracks_ids_map)
        tracks_to_display = [track for track in self.get_tracks() if track["name"] in displayed_tracks]
        # print(tracks_to_display)
        for t in tracks_to_display:
            tracks_configs.append(self.get_track_display(t))   
            # print(self.get_track_display(t))
        # for track_name in self.tracks_ids_map  
        #tracks = self.get_tracks(assembly, displayed_tracks, display_assembly)
        self.config["defaultSession"] = {
            "name": "my session",
            "view": {
                "id": "LinearGenomeView",
                "type": "LinearGenomeView",
                "tracks": tracks_configs
            }
        }

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
