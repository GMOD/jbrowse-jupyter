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

    conf.set_location("SL4.0ch00:1..9,643,250")
    assert conf.get_config()["location"] == "SL4.0ch00:1..9,643,250"

    conf.set_location("ctgA:1105..1221")
    assert conf.get_config()["location"] == "ctgA:1105..1221"


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


def test_set_assembly():
    myError = "Can not get assembly name. Please configure the assembly first."
    conf = JBrowseConfig()
    # raises exception trying to get name before setting an assembly
    with pytest.raises(Exception) as excinfo:
        conf.get_assembly_name()
    assert myError in str(excinfo)
    # raises an error if you try to add a track before an assembly is set
    data = "https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz"
    with pytest.raises(Exception) as excinfo:
        conf.add_track(
            data,
            name="test-demo",
        )
    assert "Please set the assembly before adding a track." in str(excinfo)
    # raises an error, there is no local path support in non jupyter envs
    with pytest.raises(TypeError) as excinfo:
        conf.set_assembly("/hi/there")
    err = (
        f'Path {"/hi/there"} for assembly data is used'
        ' in an unsupported environment.'
        'Paths are supported in Jupyter notebooks and Jupyter lab.'
        'Please use a url for your assembly data. You can check out '
        'our local file support docs for more information'
    )
    assert err == excinfo.value.args[0]
    aliases = ["hg38"]
    uri = "https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/hg38_aliases.txt"
    ref_name_aliases = {
        "adapter": {
            "type": "RefNameAliasAdapter",
            "location": {
                "uri": uri,
            },
        },
    }
    conf.set_assembly(
        "https://jbrowse.org/genomes/GRCh38/fasta/hg38.prefix.fa.gz",
        aliases=aliases,
        ref_name_aliases=ref_name_aliases,
    )
    err = "assembly is already set, set overwrite to True to overwrite"
    with pytest.raises(TypeError) as excinfo:
        conf.set_assembly(
            "https://another/assembly.fa.gz",
            aliases=aliases,
            ref_name_aliases=ref_name_aliases,
        )
    assert err in str(excinfo)
    assert conf.get_assembly_name() == "hg38"
    track_data = (
        "https://s3.amazonaws.com/jbrowse.org/"
        "genomes/GRCh38/ncbi_refseq/GCA_000001405.15_"
        "GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz"
    )
    conf.add_track(
        track_data,
        name="test-demo",
    )
    assert len(conf.get_tracks()) == 1

    alias_uri = "https://s3.amazonaws.com/jbrowse.org/genomes/hg19/hg19_aliases.txt"
    ref_name = {
        "adapter": {"type": "RefNameAliasAdapter", "location": {"uri": alias_uri}}
    }
    aliases = ["GRCh37"]

    a_data = "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz"
    conf.set_assembly(a_data, aliases=aliases, refname_aliases=ref_name, overwrite=True)
    assert conf.get_assembly_name() == "hg19"


def test_create_view():
    "tests creating a view from one of the provided genomes"
    genome_error = (
        '"volvox" is not a valid default genome to view.'
        "Choose from hg19 or hg38 or pass your own conf."
    )
    with pytest.raises(TypeError) as excinfo:
        create("LGV", genome="volvox")
    assert genome_error in str(excinfo)
    # creates JBrowseConfig from default hg19 or hg38
    hg19 = create("LGV", genome="hg19")
    hg38 = create("LGV", genome="hg38")
    assert hg19.get_assembly_name() == "hg19"
    assert len(hg19.get_tracks()) == 0
    assert hg19.get_default_session()
    assert hg38.get_assembly_name() == "hg38"
    assert len(hg38.get_tracks()) == 0
    assert hg38.get_default_session()


def test_create_view_invalid_genome():
    "test creating a view from a config"
    invalid_genome = "invalidGenome"
    msg = "Choose from hg19 or hg38 or pass your own conf"
    error = "is not a valid default genome to view."
    err = f'"{invalid_genome}" {error}{msg}'
    with pytest.raises(TypeError) as excinfo:
        create("view", genome="invalidGenome")
        create("invalidView")
    assert err in str(excinfo)


def test_create_view_invalid():
    "test creating a view from a config"
    error = "Currently not supporting view_type: invalidView."
    with pytest.raises(TypeError) as excinfo:
        create("invalidView")
    assert error in str(excinfo)


def test_create_view_from_conf():
    # === from config object ===
    fasta_loc = "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz"
    fai_loc = "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz.fai"
    gz_loc = "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz.gzi"
    rloc = "https://s3.amazonaws.com/jbrowse.org/genomes/hg19/hg19_aliases.txt"
    ix = "https://jbrowse.org/genomes/hg19/trix/hg19.ix"
    ixx = "https://jbrowse.org/genomes/hg19/trix/hg19.ixx"
    meta = "https://jbrowse.org/genomes/hg19/trix/meta.json"
    config1 = {
        "assembly": {
            "name": "hg19",
            "aliases": ["GRCh37"],
            "sequence": {
                "type": "ReferenceSequenceTrack",
                "trackId": "hg19-ReferenceSequenceTrack",
                "adapter": {
                    "type": "BgzipFastaAdapter",
                    "fastaLocation": {"uri": fasta_loc},
                    "faiLocation": {"uri": fai_loc},
                    "gziLocation": {"uri": gz_loc},
                },
            },
            "refNameAliases": {
                "adapter": {
                    "type": "RefNameAliasAdapter",
                    "location": {"uri": rloc},
                }
            },
        },
    }
    hg19_from_config = create("conf", conf=config1)
    assert hg19_from_config.get_config()
    # can add track
    assert len(hg19_from_config.get_tracks()) == 0
    bigwig = "https://jbrowse.org/genomes/hg19/COLO829/colo_normal.bw"
    hg19_from_config.add_track(bigwig, name="example", track_id="delete-test")
    assert len(hg19_from_config.get_tracks()) == 1
    # can set default session
    hg19_from_config.set_default_session(["example"])
    assert hg19_from_config.get_default_session()
    # can delete a track
    hg19_from_config.delete_track("delete-test")
    assert len(hg19_from_config.get_tracks()) == 0
    hg19_from_config.add_text_search_adapter(ix, ixx, meta)

    adapter_list = hg19_from_config.get_text_search_adapters()
    assert len(adapter_list) == 1

    same_adapter = (
        "Adapter already exists for given adapterId: "
        "hg19-hg19.ix-index.Provide a different adapter_id"
    )
    with pytest.raises(Exception) as excinfo:
        hg19_from_config.add_text_search_adapter(ix, ixx, meta)
    assert same_adapter in str(excinfo)
    hg19_from_config.add_text_search_adapter(ix, ixx, meta, "diff-adapter")
    adapter_after = hg19_from_config.get_text_search_adapters()
    assert len(adapter_after) == 2


def test_empty_config_lgv():
    # === empty config ===
    empty_conf = create("LGV")
    assert empty_conf.get_config()
    assembly_error = (
        "Can not get assembly name. " "Please configure the assembly first."
    )
    with pytest.raises(Exception) as excinfo:
        empty_conf.get_assembly_name()
    assert assembly_error in str(excinfo)
    empty_conf.set_env("localhost", 9999)
    current_env = empty_conf.get_env()
    assert current_env[1] == 9999


def test_empty_cgv():
    # === empty config ===
    empty_conf = create("CGV")
    assert empty_conf.get_config()
    assembly_error = (
        "Can not get assembly name. " "Please configure the assembly first."
    )
    with pytest.raises(Exception) as excinfo:
        empty_conf.get_assembly_name()
    assert assembly_error in str(excinfo)


def test_create_view_cgv():
    "tests creating a view from one of the provided genomes"
    genome_error = (
        '"volvox" is not a valid default genome to view.'
        "Choose from hg19 or hg38 or pass your own conf."
    )
    with pytest.raises(TypeError) as excinfo:
        create("CGV", genome="volvox")
    assert genome_error in str(excinfo)
    # creates JBrowseConfig from default hg19 or hg38
    hg19 = create("CGV", genome="hg19")
    hg38 = create("CGV", genome="hg38")
    in_colab = hg19.colab
    assert not in_colab
    assert hg19.get_assembly_name() == "hg19"
    assert len(hg19.get_tracks()) == 0
    assert hg19.get_default_session()
    assert hg38.get_assembly_name() == "hg38"
    # hg38 for cgv does not have tracks
    assert len(hg38.get_tracks()) == 0
    assert hg38.get_default_session()
