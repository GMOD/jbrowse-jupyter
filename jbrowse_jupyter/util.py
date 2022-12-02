import re
import os
import json
import pkg_resources
import dash_jbrowse as jb
from dash import html
from urllib.parse import urlparse
from jupyter_dash import JupyterDash


def is_url(filePath):
    """
    Checks wether or not the file path
    is a valid url.
    :param str filePath: file path/url
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


def get_name_regex(assembly_file):
    """ Returns the name of the assembly based on the assembly data file"""
    return re.search(r'(\w+)\.(?:fa|fasta|fa\.gz)$', assembly_file).group(1)


def get_default(name, view_type="LGV"):
    """Returns the configuration oject given a genome name."""
    base = pkg_resources.resource_filename("jbrowse_jupyter", "data")
    file_name = f'{base}/{name}.json'
    if view_type == "CGV":
        file_name = f'{base}/{name}_cgv.json'
    conf = {}
    with open(file_name) as json_data:
        conf = json.load(json_data)
    return conf


def create_component(conf, **kwargs):
    """
    Creates a Dash JBrowse LinearGenomeView component
    given a configuration object and optionally an id.

    e.g:

    conf = hg38.get_config()
    create_component(conf,id="hg38-test", dash_comp="CGV")
    where hg38 is an instance of JBrowseConfig

    :param obj conf: configuration object from JBrowseConfig
        instance
    :param str id: id to use in Dash component
    :param str dash_comp: (optional) dash component type to
        create. Currently supporting LGV and CGV.
        defaults to `LGV` when no dash_comp= is specified
    :return: Dash JBrowse View given dash_comp type
    :rtype: Dash JBrowse component
    """
    supported = set({"LGV", "CGV"})
    comp_id = "jbrowse-component"
    dash_comp = kwargs.get("dash_comp", "LGV")
    the_view_type = conf["defaultSession"]["view"]["type"]
    msg = "config was passed but attempting to create"
    err = "Please specify the correct dash_comp."
    if (the_view_type == "LinearGenomeView" and dash_comp == "CGV"):
        raise TypeError(f'LGV {msg} a CGV.{err}')
    if (the_view_type == "CircularView" and dash_comp == "LGV"):
        raise TypeError(f'CGV {msg} a LGV.{err}')
    if "id" in kwargs:
        comp_id = kwargs["id"]
    if dash_comp in supported:
        if dash_comp == "LGV":
            return jb.LinearGenomeView(
                id=comp_id,
                assembly=conf["assembly"],
                tracks=conf["tracks"],
                defaultSession=conf["defaultSession"],
                location=conf["location"],
                configuration=conf["configuration"],
                aggregateTextSearchAdapters=conf["aggregateTextSearchAdapters"]
            )
        # here is where we can add another view
        if dash_comp == "CGV":
            return jb.CircularGenomeView(
                id=comp_id,
                assembly=conf["assembly"],
                tracks=conf["tracks"],
                defaultSession=conf["defaultSession"],
                configuration=conf["configuration"],
            )
    else:
        raise TypeError(f'The {dash_comp} component is not supported.')


def launch(conf, **kwargs):
    """
    Launches a LinearGenomeView Dash JBrowse component in a
    server with the help of JupyterDash.

    e.g
    launch(conf, dash_comp="CGV",height=400, port=8002)

    :param obj conf: JBrowseConfiguration object to pass to
        the Dash JBrowse component
    :param str id: (optional) id to use for the Dash JBrowse
        component defaults to `jbrowse-component`
    :param str dash_comp: (optional) dash component type to
        launch. Currently supporting LGV and CGV.
        defaults to `LGV` when no dash_comp= is specified
    :param int port: (optional) port to utilize when running
        the JupyterDash app
    :param int height: (optional) the height to utilize for
        the JupyterDash app
    """
    app = JupyterDash(__name__)
    # could add other JBrowse view types e.g Circular, Dotplot
    supported = set({"LGV", "CGV"})
    dash_comp = kwargs.get("dash_comp", "LGV")

    # error for mismatching config and launch type
    the_view_type = conf["defaultSession"]["view"]["type"]
    msg = "config was passed but attempting to launch"
    err = "Please specify the correct dash_comp."
    if (the_view_type == "LinearGenomeView" and dash_comp == "CGV"):
        raise TypeError(f'LGV {msg} a CGV.{err}')
    if (the_view_type == "CircularView" and dash_comp == "LGV"):
        raise TypeError(f'CGV {msg} a LGV.{err}')
    comp_id = "jbrowse-component"
    comp_port = 8050
    comp_host = '127.0.0.1'
    comp_height = 300
    comp_mode = 'inline'
    if "id" in kwargs:
        comp_id = kwargs["id"]
    if "port" in kwargs:
        comp_port = kwargs["port"]
    if "host" in kwargs:
        comp_host = kwargs["host"]
    if "height" in kwargs:
        comp_height = kwargs["height"]
    if "mode" in kwargs:
        comp_mode = kwargs["mode"]

    if dash_comp in supported:
        if dash_comp == "LGV":
            # create jupyter dash app layout
            adapters = conf["aggregateTextSearchAdapters"]
            app.layout = html.Div([
                jb.LinearGenomeView(
                    id=comp_id,
                    assembly=conf["assembly"],
                    tracks=conf["tracks"],
                    defaultSession=conf["defaultSession"],
                    aggregateTextSearchAdapters=adapters,
                    location=conf["location"],
                    configuration=conf["configuration"]
                )])
        if dash_comp == "CGV":
            # create jupyter dash app layout
            app.layout = html.Div([
                jb.CircularGenomeView(
                    id=comp_id,
                    assembly=conf["assembly"],
                    tracks=conf["tracks"],
                    defaultSession=conf["defaultSession"],
                    configuration=conf["configuration"]
                )])
    else:
        raise TypeError(f'The {dash_comp} component is not supported.')
    app.run_server(port=comp_port, host=comp_host,
                   height=comp_height, mode=comp_mode, use_reloader=False)
