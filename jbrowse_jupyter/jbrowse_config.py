from jbrowse_jupyter.util import is_URL,defaults
from jbrowse_jupyter.tracks import guessAdapterType, guessTrackType

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
        # TODO: adapt it to be like a react LGV view state
        if "path" in kwargs:
            with open(kwargs["path"], "r") as file:
                data = json.load(file)
                conf = data
        else:
            raise TypeError("path is required arg for viewType=JB2config")
    elif viewType == "config":
        if "conf" in kwargs:
            conf = kwargs["conf"]
        else:
            raise TypeError("conf is required arg for viewType=config")
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
        self.tracks_ids_map = {}

    def get_config(self):
        return self.config
    
    def get_tracks(self):
        return self.config["tracks"]

    def add_track(self, data, index='', local=False):
        # STEPS
        if is_URL(data):
            adapter = guessAdapterType(data, 'uri', index)
            print("ADAPTER", adapter)
            if (adapter["type"] == "UNKNOWN"): 
                raise TypeError("UNKNOWN adapter type")
            trackType = guessTrackType(adapter["type"])
            name = 'test name'
            assemblyNames = [self.get_assembly_name()]
            # TODO: check if track id in trackIds, if yes replace else add to list
            print("TRACKS", self.get_tracks())
            newTracks = self.get_tracks()

            newTracks.append(
                {
                    "type": trackType,
                    "trackId": "trackId-test",
                    "name": name,
                    "assemblyNames": assemblyNames,
                    "adapter": adapter
                }
            )
            
            self.config["tracks"] = newTracks
            print("new tracks", self.config["tracks"])
            
        else:
            raise TypeError("Local files are not currently supported.")
        
    def set_location(self, location):
        self.config["location"] = location

    def get_assembly_name(self):
        return self.config["assembly"]["name"]

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
    
    def get_reference_track(self, assembly, display_assembly):
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
