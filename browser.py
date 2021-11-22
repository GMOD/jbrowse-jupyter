import dash
import dash_jbrowse
import dash_html_components as html
from jbrowse_jupyter import JBrowseConfig, create_jbrowse

app = dash.Dash(__name__)

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

# setting the assembly
jbrowse_conf.set_assembly("https://jbrowse.org/genomes/GRCh38/fasta/hg38.prefix.fa.gz", aliases, ref_name_aliases, True)
# setting the location
jbrowse_conf.set_location("1:30..9876")
# adding a track
jbrowse_conf.add_track("https://s3.amazonaws.com/jbrowse.org/genomes/GRCh38/ncbi_refseq/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.sorted.gff.gz",True)
# grab config and create a dash component 
config = jbrowse_conf.get_config()
jb2_config_view = create_jbrowse('config', config=config)

# launch the component
app.layout = html.Div(
    [jb2_config_view],
    id='test'
)

if __name__ == "__main__":
    app.run_server(port=3000, debug=True)
