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

def test_create():
    pass
    

# TODO: finish add track test
def test_add_track():
     # TODO: tests adding track that covers diff assembly
    pass

def test_add_df_track():
     # TODO: test adding correct values for dataframe
     pass
