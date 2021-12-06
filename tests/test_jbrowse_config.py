import pytest
from jbrowse_jupyter.jbrowse_config import JBrowseConfig, create

def test_create_config():
    conf = JBrowseConfig()
    config = bool(conf.get_config()) 
    assert config is not False

def test_set_location():
    conf = JBrowseConfig()
    conf.set_location("1:1..90")
    assert conf.get_config()["location"] == "1:1..90"

def test_set_theme():
    conf = JBrowseConfig()
    conf.set_theme("#311b92")
    configuration = conf.get_config()["configuration"]
    theme = configuration["theme"]
    assert bool(theme) is not False
    primary = theme["palette"]["primary"]
    assert primary["main"] == "#311b92"
    conf.set_theme("#311b92", "#0097a7")
    secondary = conf.get_config()["configuration"]["theme"]["palette"]
    assert secondary["secondary"]["main"] == "#0097a7"

def test_set_assembly_name():
    myError = "Can not get assembly name. Please configure the assembly first."
    conf = JBrowseConfig()
    # raises exception trying to get name before setting an assembly
    with pytest.raises(Exception) as excinfo:
        conf.get_assembly_name()
    assert myError in str(excinfo)
    # raises an error if you try to add a track before an assembly is set
    with pytest.raises(Exception) as excinfo:
        conf.add_track("https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz",name="test-demo")
    assert "Please set the assembly before adding a track." in str(excinfo)
    # raises an error, there is no local file support yet
    with pytest.raises(TypeError) as excinfo:
        conf.set_assembly('./path/to/local/file', [], {})
    assert "Local files are not currently supported." in str(excinfo)
    aliases = ["hg38"]
    ref_name_aliases = {
        "adapter": {
            "type": "RefNameAliasAdapter",
            "location": {
                "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/hg38_aliases.txt",
            },
        },
    }
    conf.set_assembly("https://jbrowse.org/genomes/GRCh38/fasta/hg38.prefix.fa.gz", aliases, ref_name_aliases)
    assert conf.get_assembly_name() == 'hg38'
    conf.add_track("https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz",name="test-demo")
    assert len(conf.get_tracks()) == 1

def test_create_view():
    "tests creating a view from one of the provided genomes"
    genome_error = "volvox is not a valid default genome to view"
    with pytest.raises(TypeError) as excinfo:
        create("view", genome="volvox")
    assert genome_error in str(excinfo)
    # creates JBrowseConfig from default hg19 or hg38
    hg19 = create("view", genome="hg19")
    hg38 = create("view", genome="hg38")
    assert hg19.get_assembly_name() == 'hg19'
    assert len(hg19.get_tracks()) > 0
    assert hg19.get_default_session()
    assert hg38.get_assembly_name() == 'GRCh38'
    assert len(hg38.get_tracks()) > 0
    assert hg38.get_default_session()

def test_create_view_invalid():
    "test creating a view from a config"
    error = 'invalidView is an invalid view type, please chose from "view" or "config"'
    with pytest.raises(TypeError) as excinfo:
        create("invalidView")
    assert error in str(excinfo)

def test_create_view_from_conf():
    # === from config object ===
    config1 = {
        "assembly": {
            "name": "hg19",
            "aliases": [
                "GRCh37"
            ],
            "sequence": {
                "type": "ReferenceSequenceTrack",
                "trackId": "hg19-ReferenceSequenceTrack",
                "adapter": {
                    "type": "BgzipFastaAdapter",
                    "fastaLocation": {
                        "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz"
                    },
                    "faiLocation": {
                        "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz.fai"
                    },
                    "gziLocation": {
                        "uri": "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz.gzi"
                    }
                }
            },
            "refNameAliases": {
                "adapter": {
                    "type": "RefNameAliasAdapter",
                    "location": {
                        "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/hg19/hg19_aliases.txt"
                    }
                }
            }
        },
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
    }
    hg19_from_config = create("config",conf=config1)
    assert hg19_from_config.get_config()
    # can add track
    assert len(hg19_from_config.get_tracks()) == 0
    bigwig = "https://jbrowse.org/genomes/hg19/COLO829/colo_normal.bw"
    hg19_from_config.add_track(bigwig, name="wiggle track example")
    assert len(hg19_from_config.get_tracks()) == 1
    # can set default session
    hg19_from_config.set_default_session(['wiggle track example'])
    assert hg19_from_config.get_default_session()
    
    # === empty config ===
    empty_conf = create("config")
    assert empty_conf.get_config()
    assemblt_error = "Can not get assembly name. Please configure the assembly first."
    with pytest.raises(Exception) as excinfo:
        empty_conf.get_assembly_name()
