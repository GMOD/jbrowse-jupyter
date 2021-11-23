def parser(jb2_config):
    # attributes = ["assemblies", "tracks","configuration", "aggregateTextSearchAdapters", "defaultSession"]
    # jb2Config = [jb2_config[k] if k in jb2_config else None for k in attributes]
    assembly = default_assembly(jb2_config['assemblies'])
    assembly_name = assembly["name"]
    tracks = filter_tracks(jb2_config['tracks'], assembly_name)
    session = jb2_config['defaultSession']
    print("============= tracks", tracks)
    print("\n")
    print("============ assembly", assembly)
    return {
        "assembly": assembly,
        "tracks": [],
        "defaultSession": {
        "name": "default-session",
            "view": {
                "id": 'linearGenomeView',
                "type": 'LinearGenomeView',
                "tracks":[]
            }
        },
        "location": ""
    }

def filter_tracks(tracks, assembly_name):
    supported = {'AlignmentsTrack', 'QuantitativeTrack', 'VariantTrack', 'FeatureTrack', 'ReferenceSequenceTrack'}
    return [track for track in tracks if assembly_name in track["assemblyNames"] and track["type"] in supported]

def filter_txt_search_adapters(adapters, assembly_name):
    return [adapter for adapter in adapters if assembly_name in track["assemblyNames"]]

def format_config(configuration):
    if configuration['theme']:
        return {
            theme: configuration["theme"]
        }
    return {}

def default_session(default_session):
    # TODO: find a way to parse default session
    session = {
        "name": "default-session",
        "view": {
            "id": 'linearGenomeView',
            "type": 'LinearGenomeView',
            "tracks":[]
        }
    }     
    return session

def default_assembly(assemblies):
    if assemblies:
        return assemblies[0]
    else:
        raise TypeError('Invalid JBrowse2 config, missing assemblies.')
