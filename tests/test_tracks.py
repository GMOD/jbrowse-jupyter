import pytest
import pandas as pd
from jbrowse_jupyter.tracks import make_location, check_track_data, check_track_data, get_track_data
from jbrowse_jupyter.jbrowse_config import create

cram = "https://s3.amazonaws.com/jbrowse.org/genomes/hg19/skbr3/reads_lr_skbr3.fa_ngmlr-0.2.3_mapped.down.cram"
bam = "https://s3.amazonaws.com/jbrowse.org/genomes/hg19/amplicon_deep_seq/out.marked.bam"
gff3 = 'https://s3.amazonaws.com/jbrowse.org/genomes/hg19/ncbi_refseq/GRCh37_latest_genomic.sort.gff'
gff3Tabix = 'https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz'
vcf = 'https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf'
vcfGz = 'https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz'
bigWig = 'http://hgdownload.cse.ucsc.edu/goldenpath/hg38/phyloP100way/hg38.phyloP100way.bw'

def test_make_location():
    with pytest.raises(TypeError) as excinfo:
        make_location("https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf", "local")
    assert "invalid protocol local" in str(excinfo)

def test_add_track_fail():
    conf = create("config")
    assembly_error = "Please set the assembly before adding a track."
    with pytest.raises(Exception) as excinfo:
        conf.add_track(gff3, name="this will fail")
    assert assembly_error in str(excinfo)

def test_alignments():
    conf = create("view", genome="hg19")
    # BAM or CRAM alignment data
    conf.add_track(cram, name="alignments cram track example")
    conf.add_track(bam, name="alignments bam track example")
    cram_track = conf.get_track("alignments cram track example")
    bam_track = conf.get_track("alignments bam track example")
    assert cram_track[0]["type"] == "AlignmentsTrack"
    assert bam_track[0]["type"] == "AlignmentsTrack"

def test_feature():
    conf = create("view", genome="hg19")
    track_error = "Adapter type is not recognized"
    # gff is not supported
    with pytest.raises(TypeError) as excinfo:
        conf.add_track(gff3, name="gff feature")
    assert track_error in str(excinfo)
    # gff3 is supported
    conf.add_track(gff3Tabix, name="gff3 feature")
    gff3_track = conf.get_track("gff3 feature")
    assert gff3_track[0]["type"] == "FeatureTrack"

def test_variant():
    # VCF data
    conf = create("view", genome="hg19")
    conf.add_track(vcf, name="vcf track")
    conf.add_track(vcfGz, name="vcfgz track")
    vcf_track = conf.get_track("vcfgz track")
    assert vcf_track[0]["type"] == "VariantTrack"

def test_wiggle():
    # bigWig data (quantitative/wiggle)
    conf = create("view", genome="hg19")
    conf.add_track(bigWig, name="wiggle track")
    bigwig_track = conf.get_track("wiggle track")
    assert bigwig_track[0]["type"] == "QuantitativeTrack"


# ==== dataframe track ======
def test_data_frame_track():
    hg38 = create('view', genome='hg38')
    assert len(hg38.get_tracks()) == 1
    data_frame = { 'refName': ["1", "1"], 'start': [123, 456], 'end': [780, 101112], 'name': ['feature1', 'feature2']}  
    df = pd.DataFrame(data_frame)
    hg38.add_df_track(df, 'data_frame_track_name')
    data_empty = {'refName': [], 'start': [], 'end': [], 'name': [], 'score': []}
    assert len(hg38.get_tracks()) == 2
    # throw error if the dataframe is empty
    df_empty = pd.DataFrame(data_empty)
    df_error = "DataFrame must not be empty."
    with pytest.raises(TypeError) as excinfo:
        hg38.add_df_track(df_empty, 'empty_data_frame_track')
    assert df_error in str(excinfo)

def test_check_track_data():
    df_error = "Track data must be a DataFrame"
    invalid_df = { 'refName': "1", 'start': 123, 'end': 789, 'name': 'feature1'}  
    with pytest.raises(TypeError) as excinfo:
        check_track_data(invalid_df)
    assert df_error in str(excinfo)
    data_frame = { 'refName': ["1", "1"], 'start': [123, 456], 'end': [780, 101112], 'name': ['feature1', 'feature2']}  
    df = pd.DataFrame(data_frame)

def test_check_columns():
    # missing start column
    column_error = "DataFrame must contain columns: refName, start, end, name."
    invalid_df = { 'refName': ["1", "1"], 'end': [780, 101112], 'name': ['feature1', 'feature2']}  
    df = pd.DataFrame(invalid_df)
    with pytest.raises(TypeError) as excinfo:
        check_track_data(df)
    assert column_error in str(excinfo)

def test_get_df_features():
     # TODO: test adding correct values types for dataframe
    data_frame = { 'refName': ["1", "1"], 'start': [123, 456], 'end': [780, 101112], 'name': ['feature1', 'feature2']}
    df = pd.DataFrame(data_frame)
    features =  get_track_data(df)
    assert len(features) == 2
