import json
import re
import os
import dash_html_components as html
from pathlib import Path
from dash_jbrowse import LinearGenomeView
from urllib.parse import urlparse
from jupyter_dash import JupyterDash


def is_URL(filePath):
    regex = re.compile(r'^https?:\/\/', re.IGNORECASE)
    return re.match(regex, filePath) is not None

def guess_file_name(data):
    url = urlparse(data)
    return os.path.basename(url.path)

def defaults(name):
    os.getcwd()
    fileName = Path(f'jbrowse_jupyter/data/{name}.json').resolve()
    with open(fileName, "r") as file:
        data = json.load(file)
        conf = data
        return conf

def create_component(conf):
    return LinearGenomeView(
        id="jbrowse-component",
        assembly=conf["assembly"],
        tracks=conf["tracks"],
        defaultSession=conf["defaultSession"],
        location=conf["location"],
        configuration=conf["configuration"],
    )

def launch(conf):
    app = JupyterDash(__name__)
    # TODO: verify correct div height
    app.layout = html.Div([LinearGenomeView(
            id="jbrowse-component",
            assembly=conf["assembly"],
            tracks=conf["tracks"],
            defaultSession=conf["defaultSession"],
            location=conf["location"],
        )])
    app.run_server(port=3000, height=300, mode="inline")        
