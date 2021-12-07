import re
import os
import json
import dash_html_components as html
import pkg_resources
from dash_jbrowse import LinearGenomeView
from urllib.parse import urlparse
from jupyter_dash import JupyterDash


def is_url(filePath):
    """
    Checks wether or not the file path
    is a valid url.
    :param str filePath: file path
    :return: returns true if path matches pattern starting with
    http:// or https://
    :rtype: boolean
    """
    regex = re.compile(r'^https?:\/\/', re.IGNORECASE)
    return re.match(regex, filePath) is not None


def guess_file_name(data):
    """
    Guess the file name given a path.

    :param str data: file path
    :return: the predicted file name
    :rtype: str
    """
    url = urlparse(data)
    return os.path.basename(url.path)


def get_name(assembly_file):
    """ Returns the name of the assembly based on the assembly data file"""
    name_end = 0
    name_start = 0
    for i in range(0, len(assembly_file)):
        if (
            assembly_file[len(assembly_file) - i - 1: len(assembly_file) - i]
            == "/"
        ):
            name_start = len(assembly_file) - i
            break
    for i in range(name_start, len(assembly_file)):
        if assembly_file[i: i + 1] == ".":
            name_end = i
            break

    return assembly_file[name_start:name_end]


def get_default(name):
    """Returns the configuration oject given a genome name."""
    # base = os.path.abspath(os.path.dirname(__file__))
    # fileName = os.path.join(base, f'data/{name}.json')
    base = pkg_resources.resource_filename("jbrowse_jupyter", "data")
    file_name = f'{base}/{name}.json'
    with open(file_name) as json_data:
        data = json.load(json_data)
        conf = data
        return conf


def create_component(conf, **kwargs):
    """
    Creates a Dash JBrowse LinearGenomeView component given a
        configuration object and optionally an id.
    """
    supported = set({"LGV"})
    comp_id = "jbrowse-component"
    dash_comp = kwargs.get("dash_comp", "LGV")
    if "component_id" in kwargs:
        comp_id = kwargs["component_id"]
    if dash_comp in supported:
        if dash_comp == "LGV":
            return LinearGenomeView(
                id=comp_id,
                assembly=conf["assembly"],
                tracks=conf["tracks"],
                defaultSession=conf["defaultSession"],
                location=conf["location"],
                configuration=conf["configuration"],
                aggregateTextSearchAdapters=conf["aggregateTextSearchAdapters"]
            )
        # here is where we can add another view
    else:
        raise TypeError(f'The {dash_comp} component is not supported.')


def launch(conf, **kwargs):
    """
    Launches a LinearGenomeView Dash component.

    :param obj conf: JBrowseConfiguration object to pass to
        the Dash JBrowse component
    :param str id: (optional) id to use for the Dash JBrowse
        component defaults to `jbrowse-component`
    :param int port: (optional) port to utilize when running
        the JupyterDash app dash
    :param int height: (optional) the height to utilize for
        the JupyterDash app
    """
    app = JupyterDash(__name__)
    # TODO: add other JBrowse view types e.g Circular, Dotplot
    supported = set({"LGV"})
    dash_comp = kwargs.get("dash_comp", "LGV")
    comp_id = "jbrowse-component"
    comp_port = 3000
    comp_height = 300
    if "id" in kwargs:
        comp_id = kwargs["id"]
    if "port" in kwargs:
        comp_port = kwargs["port"]
    if "height" in kwargs:
        comp_height = kwargs["height"]

    if dash_comp in supported:
        if dash_comp == "LGV":
            # create jupyter dash app layout
            app.layout = html.Div([LinearGenomeView(
                    id=comp_id,
                    assembly=conf["assembly"],
                    tracks=conf["tracks"],
                    defaultSession=conf["defaultSession"],
                    location=conf["location"],
                    configuration=conf["configuration"]
                )])
    else:
        raise TypeError(f'The {dash_comp} component is not supported.')
    app.run_server(port=comp_port,
                   height=comp_height, mode="inline", use_reloader=False)
