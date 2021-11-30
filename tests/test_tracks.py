import pytest
from jbrowse_jupyter.tracks import make_location


# def test_guess_adapter():    
#     bigBed = 'https://hgdownload.soe.ucsc.edu/gbdb/hg38/bbi/clinGen/clinGenGeneDisease.bb'
#     protocol = 'uri'
#     pass

def test_alignments():
    # TODO: 
    # BAM or CRAM alignment data
    cram = 'https://s3.amazonaws.com/jbrowse.org/genomes/hg19/hg002/HG002_ONTrel2_16x_RG_HP10xtrioRTG.cram'
    bam = 'https://jbrowse.org/genomes/GRCh38/repeats.bb'
    pass

def test_feature():
    # TODO: 
    # visualize GFF3 data
    gff3 = 'https://s3.amazonaws.com/jbrowse.org/genomes/hg19/ncbi_refseq/GRCh37_latest_genomic.sort.gff'
    gff3Tabix = 'https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz'
    pass

def test_variant():
    # TODO: 
    # VCF data
    vcf = 'https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf'
    vcfGz = 'https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz'
    pass

def test_wiggle():
    # TODO:
    # bigWig data (quantitative is wiggle)
    bigWig = 'http://hgdownload.cse.ucsc.edu/goldenpath/hg38/phyloP100way/hg38.phyloP100way.bw'
    pass

def test_make_location():
    with pytest.raises(TypeError) as excinfo:
        make_location("https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf", "local")
    assert "invalid protocol local" in str(excinfo)
    
# ==== dataframe track ======
# TODO: test datafram utility functions
def test_data_frame_track():
    pass

def test_check_columns():
    pass

def test_format_features():
    pass

def test_from_config_adapter():
    pass

def test_get_df_track_data():
    pass
