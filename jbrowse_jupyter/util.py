import dash_jbrowse
import json
import re
import os
from pathlib import Path


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

def create_component(conf):
    return dash_jbrowse.DashJbrowse(
        id="jbrowse-component",
        assembly=conf["assembly"],
        tracks=conf["tracks"],
        defaultSession=conf["defaultSession"],
        location=conf["location"],
    )
