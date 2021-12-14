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
    Creates a JBrowseConfig given a view type.

    :param str view_type: the type of view ('view' or 'conf')
    :param str genome: genome ('hg19' or 'hg38')
        for view type `view`
    :return: JBrowseConfig
    :rtype: JBrowseConfig instance
    :raises TypeError: if genome passed is not hg19 or hg38
    :raises TypeError: if genome is not passed when choosing view_type `view`
    :raises TypeError: if view type is not `view` or `conf`
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
    """
    Creates Browse configuration objects.
    Currently supporting configuration objects for the
    React JBrowse Linear Genome View
    https://jbrowse.org/storybook/lgv/main
    """
    def __init__(self, conf=None):
        """
        Initializes class.

        :param obj conf: optional conf obj
        """
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

    def get_config(self):
        """
        Returns the configuration object of the JBrowseConfig
        instance. This object can then be passed to launch or
        create_component to launch or create a Dash JBrowse
        component (currently only supporting LinearGenomeView)

        e.g: create("view", genome="hg19").get_config()

        :return: returns configuration object
        :rtype: obj
        """
        return self.config

    # ========== Assembly ===========

    def get_assembly(self):
        # Returns the JBrowseConfig assembly subconfiguration object
        return self.config["assembly"]

    def get_assembly_name(self):
        # Returns the assembly name.
        assembly_error = "Can not get assembly name. " \
            "Please configure the assembly first."
        if self.get_assembly():
            return self.get_assembly()["name"]
        else:
            raise Exception(assembly_error)

    def set_assembly(self, assembly_data, **kwargs):
        """
        Sets the assembly.

        Assumes assembly_data.fai exists for fasta assembly data
        that is not bgzipped.

        Assumes assembly_data.fai and assembly_data.gzi exist for
        bgzipped assembly data.

        e.g set_assembly("url/assembly.fasta.gz", overwrite=True)
        assumes
        "url/assembly.fasta.gz.fai" and
        "url/assembly.fasta.gz.gzi" also exist

        For configuring assemblies check out our config docs
        https://jbrowse.org/jb2/docs/config_guide/#assembly-config

        :param str assembly_data: path to the sequence data
        :param str name: (optional) name for the assembly,
            defaults to name generated from assembly_data file name
        :param list aliases: (optional) list of aliases for the assembly
        :param obj refname_aliases: (optional) config for refname aliases.
        :param str overwrite: flag wether or not to overwrite
            existing assembly, default to False.
        :raises TypeError: if assembly_data is a local file
        :raises TypeError: adapter used for file type is not supported or
            recognized
        """
        overwrite = kwargs.get('overwrite', False)
        indx = kwargs.get('index', "defaultIndex")
        err = 'assembly is already set, set overwrite to True to overwrite'
        if self.get_assembly() and not overwrite:
            raise TypeError(err)
        aliases = kwargs.get('aliases', [])
        refname_aliases = kwargs.get('refname_aliases', {})
        if (is_url(assembly_data)):
            if (indx != 'defaultIndex'):
                if not is_url(indx):
                    raise TypeError("Local files are not currently supported")
            name = kwargs.get('name', get_name(assembly_data))
            assembly_adapter = guess_adapter_type(assembly_data, 'uri', indx)
            if (assembly_adapter["type"] == "UNKNOWN"):
                raise TypeError("Adapter type is not recognized")
            if (assembly_adapter["type"] == "UNSUPPORTED"):
                raise TypeError("Adapter type is not supported")
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
        # Returns the reference track for the configured assembly.
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
        # Returns the track display subconfiguration.
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
        # Return the list of track configurations with that name
        tracks = [track for track in self.get_tracks() if track["name"]
                  == track_name]
        return tracks

    def get_tracks(self):
        # Returns list of tracks in the configuration.
        return self.config["tracks"]

    def add_df_track(self, track_data, name, **kwargs):
        """
        Adds track from a pandas DataFrame. If the score column
        is present, it will create a Quantitative track else it
        will create a Feature track.

        Requires DataFrame to have columns named 'refName',
        'start', 'end', and 'name'

        Requires refName and name columns to be of type str and
        start, end, and score to be int

        e.g:
        add_df_track(df, "track_name")

        :param df: panda DataFrame with the track data.
        :param str name: name for the track.
        :param str track_id: (optional) trackId for the track
        :param str overwrite: flag wether or not to overwrite existing track.
        :raises Exception: if assembly has not been configured.
        :raises TypeError: if track data is invalid
        :raises TypeError: if track with that trackId already exists
            list of tracks
        """
        if not self.get_assembly():
            raise Exception("Please set the assembly before adding a track.")
        check_track_data(track_data)

        overwrite = kwargs.get('overwrite', False)
        assembly_name = self.get_assembly_name()
        track_id = kwargs.get('track_id', f'{assembly_name}-{name}')
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
            # delete track and overwrite it
            current_tracks = [
                t for t in current_tracks if t["trackId"] != track_id]

        current_tracks.append(df_track_config)
        self.config["tracks"] = current_tracks
        self.tracks_ids_map[track_id] = df_track_config

    def add_track(self, data, **kwargs):
        """
        Adds a track subconfiguration to the list of tracks
        in the config.

        if an index is not provided, it will assume an index file
        with the same name  can be found in the directory of the
        track data

        e.g:
        add_track("url.bam")
        assumes "url.bam.bai" also exists

        :param str data: track file or url
            (currently only supporting url)
        :param str name: (optional) name for the track
            (defaults to data filename)
        :param str track_id: (optional) trackId for the track
        :param str index: (optional) index file for the track
        :param str track_type: (optional) track type
        :param boolean overwrite: (optional) defaults to False
        :raises Exception: if assembly has not been configured
        :raises TypeError: if track data is not provided
        :raises TypeError: if track type is not supported
        """
        # TODO: local file support
        # TODO: get effective/working locations for track data
        # and track index when
        if not data:
            raise TypeError(
                "A path to the track data is required. None was provided.")
        if not self.get_assembly():
            raise Exception("Please set the assembly before adding a track.")

        assembly_names = [self.get_assembly_name()]
        name = kwargs.get('name', guess_file_name(data))
        index = kwargs.get('index', "defaultIndex")
        overwrite = kwargs.get('overwrite', False)
        current_tracks = self.get_tracks()
        if is_url(data):
            # default to uri protocol until local files enabled
            if not is_url(index) and index != "defaultIndex":
                raise TypeError("Local files are not currently supported."
                                "Provide a url for your index file.")
            adapter = guess_adapter_type(data, 'uri', index)
            if (adapter["type"] == "UNKNOWN"):
                raise TypeError("Adapter type is not recognized")
            if (adapter["type"] == "UNSUPPORTED"):
                raise TypeError("Adapter type is not supported")
            # get sequence adapter for cram adapter track
            if adapter["type"] == "CramAdapter":
                extra_config = self.get_assembly()["sequence"]["adapter"]
                adapter["sequenceAdapter"] = extra_config
            t_type = kwargs.get('track_type',
                                guess_track_type(adapter["type"]))
            supported_track_types = set({
                'AlignmentsTrack',
                'QuantitativeTrack',
                'VariantTrack',
                'FeatureTrack',
                'ReferenceSequenceTrack'
            })
            if t_type not in supported_track_types:
                raise TypeError(f'Track type: "{t_type}" is not supported.')
            default_track_id = f'{self.get_assembly_name()}-{name}'
            track_id = kwargs.get('track_id', default_track_id)
            track_config = {
                "type": t_type,
                "trackId": track_id,
                "name": name,
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

            current_tracks.append(track_config)
            self.config["tracks"] = current_tracks
            self.tracks_ids_map[track_id] = track_config
        else:
            raise TypeError("Local files are not currently supported.")

    # ======= location ===========
    def set_location(self, location):
        """
        Sets initial location for when the browser first loads.

        e.g:
        set_location("chr1:1..90")

        :param str location: location, syntax 'refName:start-end'
        """
        self.config["location"] = location

    # ======= default session ========
    def set_default_session(self, tracks_ids, display_assembly=True):
        """
        Sets the default session given a list of track ids

        e.g:
        set_default_session(['track_id', 'track_id2'])

        :param tracks_ids: list[str] list of track ids to display
        :param boolean display_assembly: display the assembly reference
            sequence track. Defaults to True
        :raises Exception: if assembly has not been configured
        """
        err = "Please set the assembly before setting the default session."
        if not self.get_assembly():
            raise Exception(err)
        reference_track = {}
        tracks_configs = []
        if (display_assembly):
            reference_track = self.get_reference_track()
            tracks_configs.append(reference_track)
        tracks_to_display = [
            t for t in self.get_tracks() if t["trackId"] in tracks_ids]
        # guess the display type
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
        # Returns the defaultSession subconfiguration
        return self.config["defaultSession"]

    # ====== Advanced Customization ===============
    def get_text_search_adapters(self):
        # Returns the aggregateTextSearchAdapters in the config
        return self.config["aggregateTextSearchAdapters"]

    def add_text_search_adapter(self, ix_path,
                                ixx_path, meta_path, adapter_id=None):
        """
        Adds an aggregate trix text search adapter.

        e.g:
        add_text_search_adapter("url/file.ix", url/file.ixx",
        "url/meta.json")

        :param str ix_path: path to ix file
        :param str ixx_path: path to ixx file
        :param str meta_path: path to meta.json file
        :param str adapter_id: optional adapter_id
        :raises Exception: if assembly has not been configured
        :raises TypeError: if adapter with same adapter id
                is already configured
        :raises TypeError: local files are not supported
        """
        err = "Please set the assembly before adding a text search adapter."
        if not self.get_assembly():
            raise Exception(err)
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
            raise TypeError("Adapter already exists for given adapterId: "
                            f'{text_id}.Provide a different adapter_id'
                            )
        adapters.append(text_search_adapter)
        self.config["aggregateTextSearchAdapters"] = adapters

    def get_theme(self):
        # Returns the theme subconfiguration.
        subconfiguration = self.config["configuration"]
        return subconfiguration["theme"]

    def set_theme(self, primary,
                  secondary=None, tertiary=None, quaternary=None):
        """
        Sets the theme in the configuration. Accepts up to 4
        hexadecimal colors.

        e.g:
        set_theme("#311b92", "#0097a7", "#f57c00", "#d50000")

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
