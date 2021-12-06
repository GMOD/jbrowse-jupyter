from jbrowse_jupyter.util import is_url, get_default, guess_file_name, get_name
from jbrowse_jupyter.tracks import (
    guess_adapter_type,
    guess_track_type,
    check_track_data,
    get_from_config_adapter,
    guess_display_type
)


def create(view_type, **kwargs):
    """
    Creates a JBrowseConfig configuration object given a view type.

    Note: currently not supporting view type JB2config

    :param str view_type: the type of view (view, conf)
    :param str genome: genome to choose for view type `view`
    :return: JBrowseConfig configuration object
    :rtype: obj
    :raises TypeError:
        if genome passed is not hg19 or hg38
        if genome is not passed when choosing view type `view`
        if view type is not `view` or `conf`
    """
    available_genomes = {"hg19", "hg38"}
    conf = {}
    if view_type == "view":
        if "genome" in kwargs:
            genome = kwargs["genome"]
            if genome in available_genomes:
                conf = get_default(genome)
            else:
                raise TypeError(
                    f'{genome} is not a valid default genome to view')
        else:
            raise TypeError("genome is required arg for view_type=view")
    elif view_type == "JB2config":
        raise TypeError("currently not supporting JB2 configs files")
    elif view_type == "config":
        if "conf" in kwargs:
            conf = kwargs["conf"]
        else:
            # default empty JBrowse config
            return JBrowseConfig()
    else:
        err = f'{view_type} is an invalid view type.' \
            "Please choose view or config"
        raise TypeError(err)
    return JBrowseConfig(conf=conf)


class JBrowseConfig:
    def __init__(self, conf=None):
        # TODO: make sure all fields are passed to conf if conf is not None
        default = {
            "assembly": {},
            "tracks": [],
            "defaultSession": {
                "name": "default-session",
                "view": {
                    "id": 'linearGenomeView',
                    "type": 'LinearGenomeView',
                    "tracks": []
                }
            },
            "aggregateTextSearchAdapters": [],
            "location": "",
            "configuration": {
                "theme": {}
            }
        }
        if conf is not None:
            for r in default.keys():
                if r not in conf:
                    conf[r] = default[r]
        self.config = default if conf is None else conf
        if conf is not None:
            ids = {x["trackId"]: x for x in conf["tracks"]}
            self.tracks_ids_map = ids
        self.tracks_ids_map = {}
        # print("trackIds map", self.tracks_ids_map.keys())

    def get_config(self):
        """ Returns the JBrowseConfig configuration object."""
        return self.config

    # ========== Assembly ===========

    def get_assembly(self):
        """ Returns the JBrowseConfig assembly subconfiguration object. """
        return self.config["assembly"]

    def get_assembly_name(self):
        """
        Returns the assembly name.
        :return: assembly name
        :rtype: str
        :raises Exception: if assembly has not been configured.
        """
        assembly_error = "Can not get assembly name. " \
            "Please configure the assembly first."
        if self.get_assembly():
            return self.get_assembly()["name"]
        else:
            raise Exception(assembly_error)

    def set_assembly(self, assembly_data, aliases, refname_aliases):
        """
        Sets the assembly.

        :param str assembly_data: path to the assembly data
        :param list aliases: list of aliases for the assembly
        :param obj refname_aliases: configuration for refname aliases.
        :return: assembly name
        :rtype: str
        :raises TypeError: if assembly_data is a local file
        """
        # TODO: test two bit adapter and other supported assembly types
        if (is_url(assembly_data)):
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
        Returns the reference track for the configured assembly.
        """
        assembly_name = self.get_assembly_name()
        configuration = f'{assembly_name}-ReferenceSequenceTrack'
        conf_str = f'{configuration}-LinearReferenceSequenceDisplay'
        return {
            "type": "ReferenceSequenceTrack",
            "configuration": configuration,
            "displays": [
                {
                    "type": "LinearReferenceSequenceDisplay",
                    "configuration": conf_str,
                }
            ],
        }

    def get_track_display(self, track):
        """ Returns the track display subconfiguration"""
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

    def get_track(self, track_name):
        """ Return the list of track configurations with that name. """
        tracks = [track for track in self.get_tracks() if track["name"]
                  == track_name]
        return tracks

    def get_tracks(self):
        """ Returns list of tracks in the configuration. """
        return self.config["tracks"]

    def add_df_track(self, track_data, name, **kwargs):
        """
        Adds a track from a data frame. If the score column is present,
        it will creaet a Quantitative track else it will create a Feature
        track.

        :param df: panda DataFrame with the track data.
        :param str name: name for the track.
        :param str overwrite: flag wether or not to overwrite existing track.
        :raises Exception: if assembly has not been configured.
        :raises TypeError:
            if track data is invalid
            if track with that trackId already exists in the configuration
        """
        # TODO: test adding correct values types for dataframe
        if not self.get_assembly():
            raise Exception("Please set the assembly before adding a track.")
        check_track_data(track_data)

        overwrite = kwargs.get('overwrite', False)
        assembly_name = self.get_assembly_name()
        track_id = f'{assembly_name}-{name}'
        current_tracks = self.config["tracks"]
        # if score column is present => QuantitativeTrack, else FeatureTrack
        track_type = "FeatureTrack"
        if "score" in track_data:
            track_type = "QuantitativeTrack"

        adapter = get_from_config_adapter(track_data)
        df_track_config = {
            "type": track_type,
            "trackId": track_id,
            "name": name,
            "assemblyNames": [assembly_name],
            "adapter": adapter
        }
        err = (
            f'track with trackId: "{track_id}" already exists in config.',
            'Set overwrite to True if you want to overwrite it.'
        )
        if track_id in self.tracks_ids_map.keys() and not overwrite:
            raise TypeError(err)
        if track_id in self.tracks_ids_map.keys() and overwrite:
            # old_tracks = self.get_tracks()
            # delete track and overwrite it
            current_tracks = [
                t for t in current_tracks if t["trackId"] != track_id]

        # new_tracks = self.get_tracks()
        # new_tracks.append(df_track_config)
        current_tracks.append(df_track_config)
        self.config["tracks"] = current_tracks
        # set new config in dictionary of tracks
        self.tracks_ids_map[track_id] = df_track_config

    def add_track(self, data, **kwargs):
        """
        Adds a track subconfiguration to the list of tracks
        in the config.

        :param str data: Track file or URL
            (currently only supporting URL)
        :param str name: (optional) name for the track
            (defaults to data filename)
        :param str index: (optional) index file for the track
            (default None)
        :param boolean local: (optional) is the track data a local file
            (default False)
        :param boolean overwrite: (optional) overwrites existing track
            if it exists in list of tracks (default False)
        :raises TypeError: if track data is not provided or track type
            not supported
        """
        # TODO: have the ability to choose a track
        # TODO: have ability to provide path to index file
        # TODO: local file support
        # TODO: get effective/working locations for track data
        # and track index when
        if not data:
            raise TypeError(
                "A path to the track data is required. None was provided.")
        # check that the assembly is configured
        if not self.get_assembly():
            raise Exception("Please set the assembly before adding a track.")

        assembly_names = [self.get_assembly_name()]
        # local = kwargs.get('local', False)
        name = kwargs.get('name', None)
        # index = kwargs.get('index', None)
        overwrite = kwargs.get('overwrite', False)
        current_tracks = self.get_tracks()
        # useIndex = is_url(index) if index is not None else False
        # argsTrack = location = path/data
        if is_url(data):
            # default to uri protocol until local files enabled
            adapter = guess_adapter_type(data, 'uri', "defaultIndex")
            if (adapter["type"] == "UNKNOWN"):
                raise TypeError("Adapter type is not recognized")
            if (adapter["type"] == "UNSUPPORTED"):
                raise TypeError("Adapter type is not supported")

            if adapter["type"] == "CramAdapter":
                # get sequence adapter for cram adapter track
                extra_config = self.get_assembly()["sequence"]["adapter"]
                adapter["sequenceAdapter"] = extra_config
            # make sure track type is one of the supported track types
            track_type = guess_track_type(adapter["type"])
            supported_track_types = set({
                'AlignmentsTrack',
                'QuantitativeTrack',
                'VariantTrack',
                'FeatureTrack',
                'ReferenceSequenceTrack'
            })
            if track_type not in supported_track_types:
                raise TypeError("Track type is not supported")

            track_id = f'{self.get_assembly_name()}-{guess_file_name(data)}'
            track_name = track_id if name is None else name
            track_config = {
                "type": track_type,
                "trackId": track_id,
                "name": track_name,
                "assemblyNames": assembly_names,
                "adapter": adapter
            }
            if track_id in self.tracks_ids_map.keys() and not overwrite:
                raise TypeError(
                    (
                        f'track with trackId: "{track_id}" already exists in'
                        f'config. Set overwrite to True to overwrite it.')
                    )
            if track_id in self.tracks_ids_map.keys() and overwrite:
                current_tracks = [
                    t for t in current_tracks if t["trackId"] != track_id]

            # print('===== Debugging ======\n')
            # print(f'Name is: {trackName}')
            # print(f'Type is: {trackType}')
            # print(f'TrackId is: {trackId}')
            # print(f'Assembly name(s) is: {assemblyNames}')

            current_tracks.append(track_config)
            # self.config["tracks"] = newTracks
            self.config["tracks"] = current_tracks
            self.tracks_ids_map[track_id] = track_config
        else:
            raise TypeError("Local files are not currently supported.")

    # ======= location ===========
    def set_location(self, location):
        """ Returns the location subconfiguration. """
        self.config["location"] = location

    # ======= default session ========
    def set_default_session(self, tracks_names, display_assembly=True):
        """
        Sets the default session given a list of tracks to display.

        :param tracks_names: list[str] list of track names to display
        :param boolean display_assembly: display the assembly reference
            sequence track. Defaults to True
        """
        reference_track = {}
        tracks_configs = []
        if (display_assembly):
            reference_track = self.get_reference_track()
            tracks_configs.append(reference_track)
        tracks_to_display = [
            t for t in self.get_tracks() if t["name"] in tracks_names]
        # TODO: check if track configs work instead of the displays
        for t in tracks_to_display:
            tracks_configs.append(self.get_track_display(t))
        self.config["defaultSession"] = {
            "name": "my session",
            "view": {
                "id": "LinearGenomeView",
                "type": "LinearGenomeView",
                "tracks": tracks_configs
            }
        }

    def get_default_session(self):
        """ Returns the defaultSession subconfiguration. """
        return self.config["defaultSession"]

    # ====== Advanced Customization ===============
    def get_text_search_adapters(self):
        """ Returns the aggregateTextSearchAdapters in the config. """
        return self.config["aggregateTextSearchAdapters"]

    def add_text_search_adapter(self, ix_path,
                                ixx_path, meta_path, adapter_id=None):
        """ Adds a trix text search adapter to the root level config. """
        if not self.get_assembly():
            raise Exception("Please set the assembly before adding a track.")
        if (not (is_url(ix_path) and is_url(ixx_path) and is_url(meta_path))):
            raise TypeError("Local files are not currently supported.")
        assembly_name = self.get_assembly_name()
        default_id = f'{assembly_name}-{guess_file_name(ix_path)}-index'
        text_id = default_id if adapter_id is None else adapter_id
        text_search_adapter = {
            "type": "TrixTextSearchAdapter",
            "textSearchAdapterId": text_id,
            "ixFilePath": {
                "uri": ix_path,
                "locationType": "UriLocation"
            },
            "ixxFilePath": {
                "uri": ixx_path,
                "locationType": "UriLocation"
            },
            "metaFilePath": {
                "uri": meta_path,
                "locationType": "UriLocation"
            },
            "assemblyNames": [assembly_name]
        }
        adapters = self.get_text_search_adapters()
        exists = [a for a in adapters if a["textSearchAdapterId"] == text_id]
        if len(exists) > 0:
            raise Exception("Adapter already exists for given adapterId: "
                            f'{text_id}.Provide a different adapter_id'
                            )
        adapters.append(text_search_adapter)
        self.config["aggregateTextSearchAdapters"] = adapters

    def get_theme(self):
        """ Returns the theme subconfiguration. """
        subconfiguration = self.config["configuration"]
        return subconfiguration["theme"]

    def set_theme(self, primary,
                  secondary=None, tertiary=None, quaternary=None):
        """
        Sets the theme in the configuration given up to 4 hexadecimal colors.

        :param str primary: primary color of custom palette
        :param str secondary: (optional) secondary color
        :param str tertiary: (optional) tertiary color
        :param str quaternary: (optional) quaternary color
        """
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
