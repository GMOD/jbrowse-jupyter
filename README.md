![Pytest and flake8](https://github.com/GMOD/jbrowse-jupyter/actions/workflows/push.yml/badge.svg)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GMOD/jbrowse-jupyter/blob/main/browser.ipynb)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GMOD/jbrowse-jupyter/4ace1180f633eb5a6179c6e4f53fdbd8a436cd1e?urlpath=lab%2Ftree%2Fbinder%2Fbinder.ipynb)
[![Downloads](https://pepy.tech/badge/jbrowse-jupyter)](https://pepy.tech/project/jbrowse-jupyter)

# [JBrowse Jupyter](https://gmod.github.io/jbrowse-jupyter/)

JBrowse Jupyter is a python package that provides a python interface to JBrowse views.

The package provides a JBrowseConfig API to enable the creation of JBrowse state configuration objects. It also provides utility functions to create and embed Dash JBrowse components in jupyter notebooks and python applications.

![demo-gif](https://user-images.githubusercontent.com/45598764/144863573-2bcd982b-1d18-4dc8-aa2f-fd8adf4985a2.gif)

*You can open this browser.ipynb in colab* [here](https://colab.research.google.com/github/GMOD/jbrowse-jupyter/blob/main/browser.ipynb)
Note: to install the package in colab you can use this command.
In a new cell above the import statement
```
!pip install git+https://github.com/GMOD/jbrowse-jupyter.git@main
```
### Dash JBrowse
Dash JBrowse is a collection of dash components for JBrowse's embeddable components.

We utilize the Dash JBrowse package along with [jupyter-dash](https://github.com/plotly/jupyter-dash) library to embed [JBrowse React Linear Genome view](https://www.npmjs.com/package/@jbrowse/react-linear-genome-view) or the [JBrowse React Circular Genome view](https://www.npmjs.com/package/@jbrowse/react-circular-genome-view) in any jupyter notebook.

You can find more information about our Dash JBrowse library [here](https://github.com/GMOD/dash_jbrowse).

## Demos
* Browser notebook demo - https://colab.research.google.com/github/GMOD/jbrowse-jupyter/blob/main/browser.ipynb
* SK-BR-3 demo -  https://colab.research.google.com/github/GMOD/jbrowse-jupyter/blob/main/skbr3.ipynb

## Documentation
Additional details and tutorials can be found in our Sphinx documentation page.
https://gmod.github.io/jbrowse-jupyter/docs/html/index.html
## Installation
`jbrowse-jupyter` is freely available for download on the Python Package Index
https://pypi.org/project/jbrowse-jupyter/
### Pre-requisites
* [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) - for virtual environments
* [pip](https://packaging.python.org/en/latest/guides/installing-using-linux-tools/) - python package manager
* [Python](https://docs.python-guide.org/starting/installation/#installation) - 3.6 or greater
* [Jupyter](https://jupyter.org/install) - jupyter lab or jupyter notebook to run .ipynb files

### PyPI

```
$ pip install jbrowse-jupyter
```

### Install with conda

Clone this repository and [install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). Once you have conda installed, follow the steps found below 
to create a conda envirnment and install the dependecies.
```
$ cd jbrowse-jupyter
$ conda create -n myenv
$ conda activate myenv
$ pip install -r requirements.txt
```

## Quickstart
Install the JBrowse Jupyter package using pip
```
$ pip install jbrowse-jupyter
```

*Launching a Linear Genome View in Jupyter Notebook*
![Launching hg38 LGV in python notebook](https://github.com/GMOD/jbrowse-jupyter/raw/main/images/notebook.png)

*Launching a Circular Genome View in Jupyter Notebook*
![Launching hg19 CGV in python notebook](https://github.com/GMOD/jbrowse-jupyter/raw/main/images/notebook2.png)
*JBrowse Linear Genome view in python Dash application*
```python
from dash import html, Dash
from jbrowse_jupyter import create, create_component

app = Dash(__name__)

jbrowse_conf = create("LGV", genome="hg38")

config = jbrowse_conf.get_config()

component = create_component(config)

app.layout = html.Div(
    [component],
    id='test'
)

if __name__ == "__main__":
    app.run_server(port=8081, debug=True)
    
```

### Using jupyter-server-proxy

or using the [jupyter-server-proxy extension](https://github.com/jupyterhub/jupyter-server-proxy)
and the [jupyter-dash extension](https://github.com/plotly/jupyter-dash)

### Using Pypi
```
$ pip install jupyter-server-proxy
$ pip install jupyter-dash

```
### Using conda
```
$ conda install jupyter-server-proxy -c conda-forge
$ conda install -c conda-forge -c plotly jupyter-dash
$ jupyter lab build 
```

```python
from jupyter_dash import JupyterDash

from dash import html
from jbrowse_jupyter import create, create_component
import jupyter_server_proxy

JupyterDash.infer_jupyter_proxy_config()
#JupyterDash()._server_proxy # true if the proxy works as expected
#JupyterDash().config # gives the proxy config

app = JupyterDash(__name__)
jbrowse_conf = create("LGV", genome="hg38")

config = jbrowse_conf.get_config()
component = create_component(config)

app.layout = html.Div(
    [component],
    id='test'
)

if __name__ == "__main__":
    # the external mode should display  a url proxied by jupyter-server-proxy, 
    # very handy on jupyterlab behind jupyterhub as in departmental jupyterlab instances.
    
    app.run_server(mode='external', debug=True, port=8999)

```

![Dash JBrowse LGV in python app](https://github.com/GMOD/jbrowse-jupyter/raw/main/images/python_app.png)
You can customize the Linear Genome View by modifying the `jbrowse_conf`. The `jbrowse_conf` is an instance of our `JBrowseConfig`, and can be modified to set an assembly, add tracks, set custom color palettes and more.

Find more information about the JBrowseConfig API [here](https://gmod.github.io/jbrowse-jupyter/docs/html/index.html)

## Other Examples

You can find examples in the root of this repo, 
* `browser.py` - uses the Dash library to create a python application with the Dash JBrowse LinearGenomeView component
* `browser.ipynb` - jupyter notebook using the JupyterDash library to embed a Dash JBrowse LinearGenomeView component in a cell
* `cgv_examples.py` - uses the Dash library to create a python application with the Dash JBrowse CircularGenomeView component
* `cgv_examples.ipynb` - jupyter notebook using the JupyterDash library to embed a Dash JBrowse CircularGenomeView component in a cell
* `local_support.ipynb` - jupyter notebook with tutorial on using your local data and passing it to JBrowse views

### To run the Python Dash application
```
$ python browser.py
```
### To run the jupyter notebook

Make sure you have [jupyter notebook or jupyterlab](https://jupyter.org/install).

Within the myenv conda environment
```
$ pip install jupyterlab
```
More information on using a specific [environment in 
a jupyter notebook](https://softwarejargon.com/jupyterlab-and-conda-environment-installation-and-setup/)
## Usage
The `jbrowse-jupyter` package provides several utility functions to create and launch Dash JBrowse components in python applications and jupyter notebooks.

### Configuring Components
* `create`(view_type, **kwargs)- creates a JBrowseConfig configuration object given a view_type 
    - view_type: Choose from a LGV or CGV e.g `create`('LGV') or `create`('CGV')
    Additional params:
        - genome: choose from one of our default genomes {hg19 or hg38} e.g `create`('LGV', genome="hg38")
        OR 
        - conf: use a conf object, you can manually edit and pass json object.
        e.g `create`('LGV', conf={"my-conf": "object"})
        *Note:* you can manually create a conf following the https://jbrowse.org/jb2/docs/config_guide/
        - if no genome or conf is passed, you will create an empty JBrowseConfig for that view type.
    *defaults* if you pass no params,an empty JBrowse config for a LGV (LinearGenomeView) will be created
* `create_component`(conf, **kwargs) - creates and returns a Dash JBrowse component -> 'CGV' or 'LGV'. This component can be used as any  Dash component in Dash applications.
  - conf: JBrowseConfig obj 
  - id: id for Dash components (opyional)
  - dash_comp: 'CGV' or 'LGV', defaults to 'LGV' when none is passed
  e.g `create_component`(cgv_with_conf.get_config(), dash_comp="CGV")
* `launch`(conf, **kwargs) - launches a LinearGenomeView Dash component in a Jupyter cell
  - id: id for Dash components
  - dash_comp: 'CGV' or 'LGV', defaults to 'LGV' when none is passed
 > **Warning**: Only use `launch` in jupyter notebooks

### JBrowseConfig
Quick overview of the JBrowseConfig API

The JBrowseConfig API allows us to set an assembly, add tracks, set default sessions, set custom color themes, and more.

JBrowseConfig().
* `set_assembly`(assembly_data, aliases, refname_aliases)
    - Sets the assembly subconfiguration
    - for the refname_alias subconfiguration check out the
    JBrowse [refname aliasing docs](https://jbrowse.org/jb2/docs/config_guide/#configuring-reference-name-aliasing) 
* `add_df_track`(track_data, name, **kwargs)
    - requires DataFrame to have columns ['refName', 'start', 'end', 'name']
    - refName and name columns must be strings, start and end must be int
    - if the score column is present, it will create a Quantitative track else it will create a Feature track.
    - not available for CGV
    - params:
        * df – pandas DataFrame with the track data.
        * name (str) – (optional) name for the track
        * overwrite (str) – (optional) flag wether or not to overwrite existing track.
        * track_id (str) - (optional) trackId for the track

* `add_track`(data, **kwargs)
    - adds a track configuration given a file with track data
    - currently supporting cram, bam, vcf gzipped, gff/gff3 gzipped, bigbed, bigwig file types.
    - assumes an index exists within the same directory of the track data if no index url path is provided. 
    - currently supporting Wiggle, Variant, Feature and Alignments tracks
    - params:
        * data (str) – track file or url (currently only supporting url)
        * name (str) – (optional) name for the track
        * index (str) – (optional) index file for the track
        * track_type (str) – (optional) track type. If none is passed, the api will infer one based on the file type
        * overwrite (boolean) – (optional) overwrites existing track if it exists in list of tracks (default False)
* `delete_track`(track_id)
    - params:
        * track_id (str) - trackId for the track to delete
* `set_location`(location)
    - initial location for when the browser first loads, syntax 'refName:start-end' 
    - e.g 'chrom1:500-1000'
    - not available for CGV
* `set_default_session`(tracks_ids, display_assembly=True)
    - sets the default session given a list of track ids
    - params:
        * tracks_ids - list[str] list of track ids to display
        * display_assembly (boolean) – display the assembly reference sequence track. default=True
* `set_theme`(primary, secondary=None, tertiary=None, quaternary=None)
    - sets the theme in the configuration given up to 4 hexadecimal colors
* `add_text_search_adapter`(ix_path, ixx_path, meta_path, adapter_id=None)
    - adds a trix text search adapter
    - not available for CGV
* `get_config`() - returns the configuration object
<!-- These configurations can be used to create [Dash JBrowse's Linear Genome View](https://github.com/GMOD/dash_jbrowse) components which can be used in any python application and or jupyter notebook. -->

<!-- The JBrowseConfig API allows us to set an assembly, add tracks, set default sessions, set custom color themes, and more. -->
 <!-- For full details please reference the documentation. -->

![Circular Genome View Gif](https://user-images.githubusercontent.com/45598764/152484043-aeff48b5-a1f2-44f2-b7d9-131c2afd4e1a.gif)



### Local file support
We currently support two ways of passing your local data to JBrowse Views.

For our Jupyter users, you can leverage the Jupyter server to host your files and pass those urls to the JBrowse views. You can find a detailed example in our local_support.ipynb

For those using colab notebooks,binder, jupyter and more you can use the JBrowse dev server.

#### JBrowse dev server
We also provide a simple http server configured with CORS that will allow you to serve your local files from a specified directory within your machine.

> **_Note__** that the use of local files or the dev server provided is not recommended for production environments. 

You can spin the dev server in two ways.
1. Git clone this repo
2. From the root of this repository, you will be able to run the python file named `serve.py`
```$ python serve.py```
3. You can choose your own port, host, and directory from which to serve your files. You can also press enter to choose all the defaults. 
  - Default PORT: 8080
  - Default host: localhost
  - Default directory: the current working directory -> os.getcwd() is used

4. Now that the dev server is running you can use the url provided in the terminal to pass to your views. 
- For example: the url to the data you wish to pass to the JBrowse view config for the local dev server running on port 8080 on local host will look like this "http://localhost:8080/<your-file-name>"
e.g `jbrowse_conf.add_track("http://localhost:8080/<your-file-name>", name="test-demo")`

Or you can make your own python file and run it to start the server.

1. create a python file named dev_server.py and add the code below

```
import os
from jbrowse_jupyter import serve


if __name__ == "__main__":
    serve(os.getcwd(), port=8080, host='localhost')
```
2. Run the python file
`$ python dev_server.py`

3. This will spin up a python simple http server with cors enabled. You can take a look at our implementation of our dev server here: `jbrowse_jupyter/dev_server.py`

4. Now that the dev server is running you can use the url provided in the terminal to pass to your views. 
- For example: the url to the data you wish to pass to the JBrowse view config for the local dev server running on port 8080 on local host will look like this "http://localhost:8080/<your-file-name>"
e.g `jbrowse_conf.add_track("http://localhost:8080/<your-file-name>", name="test-demo")`



## Resources
* [JBrowse](https://jbrowse.org/jb2/) - the next generation genome browser
* [JBrowse React Linear Genome View](https://www.npmjs.com/package/@jbrowse/react-linear-genome-view) - interactive genome browser
* [JBrowse React Linear Genome View Docs](https://jbrowse.org/storybook/lgv/main/?path=/story/getting-started--page) - storybook docs of React LGV
* [Dash Applications](https://dash.plotly.com/layout) how to get started to custumize Dash applications.
* [Dash HTML components](https://dash.plotly.com/dash-html-components) Dash html components to build the Dash aplication layout.
* [DashJupyter](https://github.com/plotly/jupyter-dash) library to enable embedding Dash components in jupyter notebooks.
* [DashJbrowse](https://github.com/GMOD/dash_jbrowse) suite of Dash components for JBrowse views. (JBrowse Linear Genome View)
## Academic Use
This package was written with funding from the [NHGRI](https://genome.gov/) as
part of the JBrowse project. If you use it in an academic project that you
publish, please cite the most recent JBrowse paper, which will be linked from
[jbrowse.org](https://jbrowse.org/).
## Contact us

We **really** love talking to our users. Please reach out with any thoughts you have on what we are building!

-   Report a bug or request a feature at
    https://github.com/GMOD/jbrowse-jupyter/issues
-   Join our developers chat at https://gitter.im/GMOD/jbrowse2
-   Send an email to our mailing list at `gmod-ajax@lists.sourceforge.net`

## FAQ
* What file types are supported?
    - We currently support:
        * bam
        * big wig
        * big bed
        * cram
        * fasta indexed
        * fasta gzipped
        * gff3 tabix
        * two bit
        * vcf
        * vcf gzipped

* What track types are supported?
    - We currently support:
        * [AlignmentsTrack](https://jbrowse.org/jb2/docs/user_guide/#alignments-tracks)
        * [QuantitativeTrack](https://jbrowse.org/jb2/docs/user_guide/#bigwig-tracks)
        * [VariantTrack](https://jbrowse.org/jb2/docs/user_guide/#variant-tracks)
        * [ReferenceSequenceTrack](https://jbrowse.org/jb2/docs/user_guide/#sequence-track)
        * Feature Tracks

    For the circular genome view (CGV), we only support variant tracks. Check out [track types](https://jbrowse.org/jb2/docs/user_guide/#sequence-track) docs for more information.
* What views do you currently support?
    - We currently support JBrowse's Linear Genome View and Circular Genome View. We hope to support more in the future.
* How do I configure text searching?
    - In order to configure text searching in your Linear Genome View, you must first create a text index. Follow the steps found [here](https://jbrowse.org/jb2/docs/quickstart_cli/#indexing-feature-names-for-searching). Then you must create and add a text search adapter to your config. 
* How do I configure tracks to show up on first render?
    - You can set a specific track/tracks to show up when the component first renders, and you can do this via the default session. You can set the default session via the JBrowseConfig API. `set_default_session`
* How do I set a custom color theme palette to fit with my application?
    - You can customize the color palette of the component through the use of `set_theme` function from the JBrowseConfig API. Below is an image of an LGV with a custom color palette. 
![Custom Palette](https://github.com/GMOD/jbrowse-jupyter/raw/main/images/custom_palette.png)

* Can I use local files/my own data?
    - Yes, there are a couple of ways in which you can configure and use your own data from your local environment in jbrowse views. 
        1. Make use of the jupyter notebook/lab server. Intended for those running their notebooks with jupyter lab or jupyter notebook.
        2. Launch your own http server with CORS which will enable you to use local files. You can run our serve.py to launch our dev server. 
    (Checkout our local_support.ipynb for tutorials on how to use your own data)

**_Note_:** that these solutions are recommended for your development environments and not supported in production.
* I am running a colab notebook/binder notebook and wish to use my local data, how can I do this? 
    - You can run JBrowse dev server to serve local files to use in your JBrowse views. More information on the dev server can be found in the local file support section of this readme.
