import dash_jbrowse
import json
import re
import os
from pathlib import Path
import dash_html_components as html
from jupyter_dash import JupyterDash


def is_URL(filePath):
    regex = re.compile(r'^https?:\/\/', re.IGNORECASE)
    return re.match(regex, filePath) is not None

def guess_file_name(path):
    # TODO: implement guess file name for adding tracks
    return 'test'

def defaults(name):
    os.getcwd()
    fileName = Path(f'jbrowse_jupyter/data/{name}.json').resolve()
    with open(fileName, "r") as file:
        data = json.load(file)
        conf = data
        return conf

# def create_component(conf):
#     return dash_jbrowse.DashJbrowse(
#         id="jbrowse-component",
#         assembly=conf["assembly"],
#         tracks=conf["tracks"],
#         defaultSession=conf["defaultSession"],
#         location=conf["location"],
#     )

def launch(conf):
    app = JupyterDash(__name__)
    app.layout = html.Div([dash_jbrowse.DashJbrowse(
            id="jbrowse-component",
            assembly=conf["assembly"],
            tracks=conf["tracks"],
            defaultSession=conf["defaultSession"],
            location=conf["location"],
        )])
    app.run_server(port=3000, mode="inline")        
