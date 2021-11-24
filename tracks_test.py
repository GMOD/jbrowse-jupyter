import dash
import dash_jbrowse
import dash_html_components as html
from jbrowse_jupyter import create_jbrowse2, create_component

app = dash.Dash(__name__)

# ======== default view =========
jbrowse_conf = create_jbrowse2('view', genome="hg19")
# Add Wiggle Track
jbrowse_conf.add_track("https://jbrowse.org/genomes/hg19/COLO829/colo_normal.bw", name="wiggle track example")
# # Add Feature Track
jbrowse_conf.add_track("https://jbrowse.org/genomes/hg19/repeats.bb", name="BigBed track example")
jbrowse_conf.add_track("https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz", name="Gff Gz track example")

# Add Variant Track 
jbrowse_conf.add_track("https://s3.amazonaws.com/jbrowse.org/genomes/hg19/NA12878/NA12878_high_quality_variant.vcf.gz", name="variant track example")
# Add Alignments Track
jbrowse_conf.add_track("https://s3.amazonaws.com/jbrowse.org/genomes/hg19/skbr3/reads_lr_skbr3.fa_ngmlr-0.2.3_mapped.down.cram", name="alignments cram track example")
jbrowse_conf.add_track("https://s3.amazonaws.com/jbrowse.org/genomes/hg19/amplicon_deep_seq/out.marked.bam", name="alignments bam track example")
jbrowse_conf.set_location("chr17:41195312..41276764")
# TODO: automatically add the sequence adapter for cram
config = jbrowse_conf.get_config()

# ======= jb2 config ===========
# ========= create a dash component ==============
component = create_component(config)
# ========== launch the component ===========
app.layout = html.Div(
    [component],
    id='test'
)

if __name__ == "__main__":
    app.run_server(port=3001, debug=True)
