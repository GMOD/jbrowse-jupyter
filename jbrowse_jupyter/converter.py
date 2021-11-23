def parser(jb2_config):
    # attributes = ["assemblies", "tracks","configuration", "aggregateTextSearchAdapters", "defaultSession"]
    # jb2Config = [jb2_config[k] if k in jb2_config else None for k in attributes]
    return {
        "assembly": default_assembly(jb2_config['assemblies']),
        "tracks": filter_tracks(jb2_config['tracks']),
        "defaultSession": default_session(jb2_config['defaultSession']),
        "location": ""
    }

def filter_tracks(tracks):
    return []

def filter_txt_search_adapters(adapters):
    return []

def format_config(configuration):
    return {
        theme: {} if not configuration['theme'] else configuration['theme']
    }

def default_session(default_session):
    session = {
        "name": "default-session",
        "view": {
            "id": 'linearGenomeView',
            "type": 'LinearGenomeView',
            "tracks":[]
        }
    }     
    return session if not default_session else default_session

def default_assembly(assemblies):
    if assemblies:
        return assemblies[0]
    else:
        raise TypeError('Invalid JBrowse2 config')
