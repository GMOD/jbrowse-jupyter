import dash
import dash_jbrowse
import dash_html_components as html
from jbrowse_jupyter import JBrowseConfig, create_jbrowse2, create_component

app = dash.Dash(__name__)

# ============ create config and pass additional params =======
jbrowse_conf = JBrowseConfig()
aliases = ["hg38"]
ref_name_aliases = {
    "adapter": {
        "type": "RefNameAliasAdapter",
        "location": {
            "uri": "https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/hg38_aliases.txt",
        },
    },
}

# ============= setting the assembly ==============
jbrowse_conf.set_assembly("https://jbrowse.org/genomes/GRCh38/fasta/hg38.prefix.fa.gz", aliases, ref_name_aliases, True)


# ============== adding a track ===============
jbrowse_conf.add_track("https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz",True)
# jbrowse_conf.add_track("https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz",True)


# ======== grab config  ========
config = jbrowse_conf.get_config()

jbrowse_conf2 = create_jbrowse2('view', genome="hg38")
# config2.set_location("10:1..19999")

config2 = jbrowse_conf2.get_config()

# ========= create a dash component ==============
component = create_component(config2)

# ========== launch the component ===========
app.layout = html.Div(
    [component],
    id='test'
)

if __name__ == "__main__":
    app.run_server(port=3000, debug=True)
