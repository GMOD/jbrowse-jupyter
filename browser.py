import dash
import dash_jbrowse
import dash_html_components as html
from jbrowse_jupyter import create_jbrowse2, create_component

app = dash.Dash(__name__)

# ============ create config and pass additional params =======
jbrowse_conf = create_jbrowse2("config")
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
jbrowse_conf.add_track("https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz")
jbrowse_conf.set_location("10:1..19999")
jbrowse_conf.set_theme("#311b92", "#0097a7", "#f57c00", "#d50000")
# ======== grab config  ========
config = jbrowse_conf.get_config()


# ======== default view =========
# jbrowse_conf2 = create_jbrowse2('view', genome="hg38")
# config2 = jbrowse_conf2.get_config()
# ======= jb2 config ===========
# ========= create a dash component ==============
component = create_component(config)
# component2 = create_component(config2)
# ========== launch the component ===========
app.layout = html.Div(
    [component],
    id='test'
)

if __name__ == "__main__":
    app.run_server(port=3000, debug=True)
