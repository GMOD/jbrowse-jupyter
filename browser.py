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

jbrowse_conf.set_assembly("https://jbrowse.org/genomes/GRCh38/fasta/hg38.prefix.fa.gz", aliases, ref_name_aliases, True)
config = jbrowse_conf.get_config()
jb2_config_view = create_jbrowse('config', config=config)
print(jb2_config_view)

app.layout = html.Div(
    [jb2_config_view],
    id='test'
)

if __name__ == "__main__":
    app.run_server(debug=True)
