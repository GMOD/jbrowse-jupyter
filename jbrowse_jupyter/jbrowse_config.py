class JBrowseConfig:
    def __init__(self):
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
        }
        self.tracks_ids_map = {}

    def get_config(self):
        return self.config
        

    # def addAssembly(self, name):
    #     # def assembly(self, file, name='', aliases=[], refNameAliases=''):
    #     # TODO infer the type of the adapter based on file name
    #     # TODO infer name of the assembly based on the file name
    #     self.assembly = createAssembly2(name)
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
        print("name:" + name)
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
