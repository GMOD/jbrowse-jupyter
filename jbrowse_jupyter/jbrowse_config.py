import IPython
from jbrowse_jupyter.util import (
    is_url, get_default,
    guess_file_name,
    get_name,
)
from jbrowse_jupyter.tracks import (
    guess_adapter_type,
    guess_track_type,
    check_track_data,
    get_from_config_adapter,
    guess_display_type,
    make_url_colab_jupyter
)


def create(view_type="LGV", **kwargs):
    """
    Creates a JBrowseConfig given a view type.

    - create(): creates empty LGV JBrowseConfig
    - create("CGV"):creates empty CGV JBrowseConfig
    - create("LGV", genome="hg19"):creates LGV JBrowseConfig w/ default genome
    - create("CGV", conf={"k": "v"}):creates CGV JBrowseConfig w/ a conf obj

    :param str view_type: the type of view ('LGV' or 'CGV'), defaults to LGV
    :param str genome: genome ('hg19' or 'hg38')
    :return: JBrowseConfig
    :rtype: JBrowseConfig instance
    :raises TypeError: if genome passed is not hg19 or hg38
    :raises TypeError: if view type is not `LGV` or `CGV`
    """
    available_genomes = {"hg19", "hg38"}
    conf = kwargs.get('conf', {})
    genome = kwargs.get('genome', "empty")
    view = view_type
    # view type (LGV or CGV)
    # make it backwards compatible
    if view_type == "view" or view_type == "conf":
        view = "LGV"
    if view != "LGV" and view != "CGV":
        raise TypeError(f'Currently not supporting view_type: {view}.')
    # configuration
    # 1) genomes available
    # 2) with own conf obj OR
    # 3) empty default config to customize)
    no_configuration = (genome != "empty" and not conf)
    # Check passed genome is available
    message1 = "is not a valid default genome to view"
    message2 = "Choose from hg19 or hg38 or pass your own conf"
    if genome not in available_genomes and no_configuration:
        raise TypeError(
                    f'"{genome}" {message1}.{message2}.')
    #  genome
    if genome in available_genomes:
        conf = get_default(genome, view)
    # start from empty JBrowseConfig
    elif not conf:
        return JBrowseConfig(view=view)
    # get customized JBrowseConfig
    return JBrowseConfig(view=view, conf=conf)


class JBrowseConfig:
    """
    Creates JBrowse configuration objects.
    Currently supporting configuration objects for the
    React JBrowse Linear Genome View and React JBrowse
    Circular Genome View
    https://jbrowse.org/storybook/lgv/main
    https://jbrowse.org/storybook/cgv/main/

    """
    def __init__(self, view="LGV", conf=None):
        """
        Initializes class.

        :param str view: LGV or CGV
            defaults to LGV
        :param obj conf: optional conf obj
        """
        in_colab_notebook = False
        in_jupyter_notebook = False
        try:
            import google.colab.output # noqa
            in_colab_notebook = True
        except: # noqa
            in_colab_notebook = False
        try:
            shell = IPython.get_ipython().__class__.__name__ # noqa
            if shell == 'ZMQInteractiveShell': # noqa
                in_jupyter_notebook = True
            else:
                in_jupyter_notebook = False
        except: # noqa
            in_jupyter_notebook = False
        # =====================
        view_default = {
            "id": 'linearGenomeView',
            "type": 'LinearGenomeView',
            "tracks": []
        }
        if view != "LGV" and view == "CGV":
            view_default = {
                "id": 'circularView',
                "type": 'CircularView',
                "tracks": []
            }
        default = {
            "assembly": {},
            "tracks": [],
            "defaultSession": {
                "name": "default-session",
                "view": view_default
            },
            "aggregateTextSearchAdapters": [],
            "location": "",
            "configuration": {
                "theme": {}
            },
            # internetAccounts
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
        self.view = view
        # environment
        self.nb_port = 8888
        self.nb_host = "localhost"
        self.colab = in_colab_notebook
        self.jupyter = not in_colab_notebook and in_jupyter_notebook

    def get_config(self):
        """
        Returns the configuration object of the JBrowseConfig
        instance. This object can then be passed to launch or
        create_component to launch or create a Dash JBrowse
        component

        e.g: create("LGV", genome="hg19").get_config()

        :return: returns configuration object
        :rtype: obj
        """
        return self.config

    def get_colab(self):
        return self.colab

    def get_jupyter(self):
        return self.jupyter

    def get_env(self):
        print("notebook port: ", self.nb_port)
        print("notebook host: ", self.nb_host)
        return self.nb_host, self.nb_port

    def set_env(self, notebook_host="localhost", notebook_port=8888):
        """
        Changes the port and the host for creating links to files
        found within the file tree of jupyter.

        We want to be able to use paths to local files that can be
        accessed within the file tree of jupyter notebook and jupyter
        lab. The port and host should match those configured in your
        jupyter config.

        You can set_env after creating your view.
        browser = create("LGV")
        browser.set_env("localhost", 8989)

        :param str notebook_host: host used in jupyter config for
            for using paths to local files. (Defaults to "localhost")
        :param str notebook_port: port used in jupyter config for
            for using paths to local files. (Defaults to 8888)
        """
        self.nb_port = notebook_port
        self.nb_host = notebook_host

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

        :param str assembly_data: url/path to the sequence data
        :param str name: (optional) name for the assembly,
            defaults to name generated from assembly_data file name
        :param list aliases: (optional) list of aliases for the assembly
        :param obj refname_aliases: (optional) config for refname aliases.
        :param str overwrite: flag wether or not to overwrite
            existing assembly, default to False.
        :raises TypeError: Paths are only supported in jupyter.
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
        if is_url(assembly_data):
            if indx != 'defaultIndex':
                if not is_url(indx) and not self.jupyter:
                    raise TypeError(f'Path for {assembly_data} '
                                    "is used in an unsupported environment."
                                    "Paths are supported in Jupyter"
                                    " notebooks and Jupyter lab."
                                    "Please use a url for your assembly "
                                    "data. You can check out our local "
                                    "file support docs for more information")
            assembly_adapter = guess_adapter_type(assembly_data,
                                                  'uri',
                                                  indx,
                                                  **kwargs)
            name = kwargs.get('name', get_name(assembly_data))
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
            if not self.jupyter:
                raise TypeError(f'Path {assembly_data} for assembly data '
                                "is used in an unsupported environment."
                                "Paths are supported in Jupyter notebooks"
                                " and Jupyter lab.Please use a url for "
                                "your assembly data. You can check out "
                                "our local file support docs for more "
                                "information")
            if indx != 'defaultIndex' and not is_url(indx):
                if not self.jupyter:
                    raise TypeError("Paths are used in an "
                                    "unsupported environment."
                                    "Paths are supported in Jupyter"
                                    " notebooks and Jupyter lab."
                                    "Please use a urls for your assembly"
                                    " and index data. You can check out "
                                    "our local file support docs for more"
                                    " information")
            assembly_adapter = guess_adapter_type(assembly_data,
                                                  'localPath',
                                                  indx,
                                                  colab=self.colab,
                                                  nb_port=self.nb_port,
                                                  nb_host=self.nb_host)
            name = kwargs.get('name', get_name(assembly_data))
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
        display_type = guess_display_type(track_type, self.view)
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

        :param track_data: panda DataFrame with the track data.
        :param str name: name for the track.
        :param str track_id: (optional) trackId for the track
        :param str overwrite: flag wether or not to overwrite existing track.
        :raises Exception: if assembly has not been configured.
        :raises TypeError: if track data is invalid
        :raises TypeError: if view is not LGV
        :raises TypeError: if track with that trackId already exists
            list of tracks
        """
        if not self.get_assembly():
            raise Exception("Please set the assembly before adding a track.")
        if self.view != "LGV":
            raise TypeError("Can not add a data frame track to a CGV conf.")
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

        :param str data: track file url/path
        :param str name: (optional) name for the track
            (defaults to data filename)
        :param str track_id: (optional) trackId for the track
        :param str index: (optional) file url/path for the track
        :param str track_type: (optional) track type
        :param boolean overwrite: (optional) defaults to False
        :raises Exception: if assembly has not been configured
        :raises TypeError: if track data is not provided
        :raises TypeError: if track type is not supported
        :raises TypeError: Paths are only supported in jupyter.
        """
        if not data:
            raise TypeError(
                "Track data is required. None was provided.")
        if not self.get_assembly():
            raise Exception("Please set the assembly before adding a track.")

        assembly_names = [self.get_assembly_name()]
        name = kwargs.get('name', guess_file_name(data))
        index = kwargs.get('index', "defaultIndex")
        overwrite = kwargs.get('overwrite', False)
        current_tracks = self.get_tracks()
        if is_url(data):
            # default to uri protocol until local files enabled
            if not is_url(index) and index != 'defaultIndex':
                if not self.jupyter:
                    raise TypeError(f'Path {index} for index is used in an '
                                    "unsupported environment. Paths are "
                                    "supported in Jupyter notebooks and Jupy"
                                    "ter lab.Please use a url for your "
                                    "assembly data. You can check out "
                                    "our local file support docs for more "
                                    "information")
                else:
                    adapter = guess_adapter_type(data, 'localPath', index,
                                                 colab=self.colab,
                                                 nb_port=self.nb_port,
                                                 nb_host=self.nb_host)
            else:
                adapter = guess_adapter_type(data, 'uri', index)
            # adapter = guess_adapter_type(data, 'uri', index)
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
            if not is_url(index) and index != 'defaultIndex':
                if not self.jupyter:
                    raise TypeError(f'Path {index} for index is used in an '
                                    "unsupported environment.Paths are "
                                    "supported in Jupyter notebooks and Jupyte"
                                    "r lab.Please use a url for your assembly "
                                    "data. You can check out our local file "
                                    "support docs for more information")
            adapter = guess_adapter_type(data, 'localPath',
                                         index,
                                         colab=self.colab,
                                         nb_port=self.nb_port,
                                         nb_host=self.nb_host
                                         )
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

    def delete_track(self, track_id):
        """
        Deletes a track from the config.

        e.g:
        delte_track("test_track_id")

        Will delete track with track_id test_track_id.

        :param str track_id: track_id to delete

        :raises TypeError: if track_id provided does not exist
        """
        new_tracks = []
        current_tracks = self.get_tracks()
        if track_id not in self.tracks_ids_map.keys():
            raise TypeError(
                (
                    f'track with trackId: "{track_id}" does not exist in'
                    f'config.')
                )
        else:
            new_tracks = [
                    t for t in current_tracks if t["trackId"] != track_id]
            self.config["tracks"] = new_tracks
            # clear from default session
            default_sess = self.get_default_session()
            tracks_sess = default_sess["view"]["tracks"]
            new_tracks_sess = [
                t for t in tracks_sess if t["configuration"] != track_id]
            if (self.view == "CGV"):
                self.config["defaultSession"] = {
                    "name": "my session",
                    "view": {
                        "id": "circularView",
                        "type": "CircularView",
                        "tracks": new_tracks_sess
                    }
                }
            else:
                self.config["defaultSession"] = {
                    "name": "my session",
                    "view": {
                        "id": "LinearGenomeView",
                        "type": "LinearGenomeView",
                        "tracks": new_tracks_sess
                    }
                }

    # ======= location ===========
    def set_location(self, location):
        """
        Sets initial location for when the browser first loads.

        e.g:
        set_location("chr1:1..90")

        :param str location: location, syntax 'refName:start-end'
        :raises TypeError: if view is CGV, location not supported in CGV
        """
        if (self.view == 'CGV'):
            raise TypeError("Location is not available to set on a CGV")
        else:
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
        if (self.view == "CGV"):
            self.config["defaultSession"] = {
                "name": "my session",
                "view": {
                    "id": "circularView",
                    "type": "CircularView",
                    "tracks": tracks_configs
                }
            }
        else:
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

    def add_text_search_adapter(self, ix,
                                ixx, meta, adapter_id=None):
        """
        Adds an aggregate trix text search adapter.
        Currently not available for Circular Genome View

        e.g:
        add_text_search_adapter("url/file.ix", url/file.ixx",
        "url/meta.json")

        :param str ix: url/path to ix file
        :param str ixx: url/path to ixx file
        :param str meta: url/path to meta.json file
        :param str adapter_id: optional adapter_id
        :raises Exception: if assembly has not been configured
        :raises TypeError: if adapter with same adapter id
                is already configured
        :raises TypeError: Paths are only supported in jupyter.
        :raises TypeError: if view is CGV
        """
        err = "Please set the assembly before adding a text search adapter."
        if not self.get_assembly():
            raise Exception(err)
        local = is_url(ix) and is_url(ixx) and is_url(meta)
        if (local and not self.jupyter):
            TypeError(f'Paths for "{ix},{ixx},and {meta}"'
                      " are used in an unsupported environment. Paths are "
                      "supported in Jupyter notebooks and Jupyter lab.Please"
                      " use a url for your assembly data. You can check out"
                      " our local file support docs for more information")

        if self.view == "CGV":
            raise TypeError("Text Searching not currently available in CGV")
        assembly_name = self.get_assembly_name()
        default_id = f'{assembly_name}-{guess_file_name(ix)}-index'
        text_id = default_id if adapter_id is None else adapter_id
        text_search_adapter = {
            "type": "TrixTextSearchAdapter",
            "textSearchAdapterId": text_id,
            "ixFilePath": {
                "uri":  make_url_colab_jupyter(
                    ix,
                    colab=self.colab,
                    nb_host=self.nb_host,
                    nb_port=self.nb_port
                ),
                "locationType": "UriLocation",
            },
            "ixxFilePath": {
                "uri": make_url_colab_jupyter(
                    ixx,
                    colab=self.colab,
                    nb_host=self.nb_host,
                    nb_port=self.nb_port
                ),
                "locationType": "UriLocation",
            },
            "metaFilePath": {
                "uri": make_url_colab_jupyter(
                    meta,
                    colab=self.colab,
                    nb_host=self.nb_host,
                    nb_port=self.nb_port
                ),
                "locationType": "UriLocation",
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
