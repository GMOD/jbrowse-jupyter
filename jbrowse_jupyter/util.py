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

def get_name(assembly_file):
    """ Returns the name of the assembly based on the assembly data file"""
    name_end = 0
    name_start = 0
    for i in range(0, len(assembly_file)):
        if (
            assembly_file[len(assembly_file) - i - 1 : len(assembly_file) - i]
            == "/"
        ):
            name_start = len(assembly_file) - i
            break
    for i in range(name_start, len(assembly_file)):
        if assembly_file[i : i + 1] == ".":
            name_end = i
            break

    return assembly_file[name_start:name_end]

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
