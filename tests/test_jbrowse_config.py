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


def test_set_assembly_name():
    myError = "Can not get assembly name. Please configure the assembly first."
    conf = JBrowseConfig()
    # raises exception trying to get name before setting an assembly
    with pytest.raises(Exception) as excinfo:
        conf.get_assembly_name()
    assert myError in str(excinfo)
    # raises an error if you try to add a track before an assembly is set
    data = "https://s3.amazonaws.com/jbrowse.org/genomes/" \
        "GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_" \
        "analysis_set.refseq_annotation.sorted.gff.gz"
    with pytest.raises(Exception) as excinfo:
        conf.add_track(
            data,
            name="test-demo",
        )
    assert "Please set the assembly before adding a track." in str(excinfo)
    # raises an error, there is no local file support yet
    with pytest.raises(TypeError) as excinfo:
        conf.set_assembly("./path/to/local/file")
    assert "Local files are not currently supported." in str(excinfo)
    aliases = ["hg38"]
    uri = "https://s3.amazonaws.com/jbrowse.org/genomes/" \
        "GRCh38/hg38_aliases.txt"
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
    track_data = "https://s3.amazonaws.com/jbrowse.org/" \
        "genomes/GRCh38/ncbi_refseq/GCA_000001405.15_" \
        "GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz"
    conf.add_track(
        track_data,
        name="test-demo",
    )
    assert len(conf.get_tracks()) == 1

    alias_uri = "https://s3.amazonaws.com/jbrowse.org/genomes" \
        "/hg19/hg19_aliases.txt"
    ref_name = {
        "adapter": {
            "type": "RefNameAliasAdapter",
            "location": {
                "uri": alias_uri
            }
        }
    }
    aliases = [
        "GRCh37"
    ]

    a_data = "https://jbrowse.org/genomes/hg19/fasta/hg19.fa.gz"
    conf.set_assembly(a_data, aliases, ref_name)
    assert conf.get_assembly_name() == 'hg19'

    ref_name = {}
    aliases = []
    a_data2 = "https://s3.amazonaws.com/jbrowse.org/genomes/" \
        "tomato/SL4.0/S_lycopersicum_chromosomes.4.00.fa.gz"
    conf.set_assembly(a_data2, aliases, ref_name)
    assert conf.get_assembly_name() == 'SL4.0'


def test_create_view():
    "tests creating a view from one of the provided genomes"
    genome_error = "volvox is not a valid default genome to view"
    with pytest.raises(TypeError) as excinfo:
        create("view", genome="volvox")
    assert genome_error in str(excinfo)
    # creates JBrowseConfig from default hg19 or hg38
    hg19 = create("view", genome="hg19")
    hg38 = create("view", genome="hg38")
    assert hg19.get_assembly_name() == "hg19"
    assert len(hg19.get_tracks()) > 0
    assert hg19.get_default_session()
    assert hg38.get_assembly_name() == "GRCh38"
    assert len(hg38.get_tracks()) > 0
    assert hg38.get_default_session()


def test_create_view_invalid():
    "test creating a view from a config"
    error = "invalidView is an invalid view type.Please choose view or config"
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
                    "fastaLocation": {
                        "uri": fasta_loc
                    },
                    "faiLocation": {
                        "uri": fai_loc
                    },
                    "gziLocation": {
                        "uri": gz_loc
                    },
                },
            },
            "refNameAliases": {
                "adapter": {
                    "type": "RefNameAliasAdapter",
                    "location": {
                        "uri": rloc
                    },
                }
            },
        },
    }
    hg19_from_config = create("config", conf=config1)
    assert hg19_from_config.get_config()
    # can add track
    assert len(hg19_from_config.get_tracks()) == 0
    bigwig = "https://jbrowse.org/genomes/hg19/COLO829/colo_normal.bw"
    hg19_from_config.add_track(bigwig, name="wiggle track example")
    assert len(hg19_from_config.get_tracks()) == 1
    # can set default session
    hg19_from_config.set_default_session(["wiggle track example"])
    assert hg19_from_config.get_default_session()

    # can set text search adapter
    index_error = 'Local files are not currently supported.'
    with pytest.raises(TypeError) as excinfo:
        hg19_from_config.add_text_search_adapter(
            './path/to/ixname.ix',
            "https://path/to/ixxname.ixx",
            "https://path/to/meta.json"
        )
    assert index_error in str(excinfo)
    hg19_from_config.add_text_search_adapter(ix, ixx, meta)

    adapter_list = hg19_from_config.get_text_search_adapters()
    assert len(adapter_list) == 1

    same_adapter = "Adapter already exists for given adapterId: " \
        "hg19-hg19.ix-index.Provide a different adapter_id"
    with pytest.raises(Exception) as excinfo:
        hg19_from_config.add_text_search_adapter(ix, ixx, meta)
    assert same_adapter in str(excinfo)
    hg19_from_config.add_text_search_adapter(ix, ixx, meta, "diff-adapter")
    adapter_after = hg19_from_config.get_text_search_adapters()
    assert len(adapter_after) == 2


def test_empty_config():
    # === empty config ===
    empty_conf = create("config")
    assert empty_conf.get_config()
    assembly_error = "Can not get assembly name. " \
        "Please configure the assembly first."
    with pytest.raises(Exception) as excinfo:
        empty_conf.get_assembly_name()
    assert assembly_error in str(excinfo)
