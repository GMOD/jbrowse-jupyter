![Pytest and flake8](https://github.com/GMOD/jbrowse-jupyter/actions/workflows/push.yml/badge.svg)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GMOD/jbrowse-jupyter/blob/main/browser.ipynb)

# JBrowse Jupyter

JBrowse Jupyter is a python package that provides a python interface to JBrowse views.

The package provides a JBrowseConfig API to enable the creation of JBrowse state configuration objects. It also provides utility functions to create and embed Dash JBrowse components in jupyter notebooks and python applications.

![demo-gif](https://user-images.githubusercontent.com/45598764/144863573-2bcd982b-1d18-4dc8-aa2f-fd8adf4985a2.gif)

*You can open this browser.ipynb in colab* [here](https://colab.research.google.com/github/GMOD/jbrowse-jupyter/blob/main/browser.ipynb)
## Dash JBrowse
Dash JBrowse is a collection of dash components for JBrowse's embeddable components.

We utilize the Dash JBrowse package along with [jupyter-dash](https://github.com/plotly/jupyter-dash) library to embed [Jbrowse React Linear Genome view](https://www.npmjs.com/package/@jbrowse/react-linear-genome-view) in any jupyter notebook.

You can find more information about our Dash JBrowse library [here](https://github.com/GMOD/dash_jbrowse).

## Quickstart
Install the JBrowse Jupyter package using pip
```
$ pip install jbrowse-jupyter
```

*Launching a Linear Genome View in Jupyter Notebook*
![Launching hg38 LGV in python notebook](./images/notebook.png)

*JBrowse Linear Genome view in python Dash application*
```python
import dash
import dash_jbrowse
import dash_html_components as html
from jbrowse_jupyter import create, create_component

app = dash.Dash(__name__)

jbrowse_conf = create("view", genome="hg38")

config = jbrowse_conf.get_config()

component = create_component(config)

app.layout = html.Div(
    [component],
    id='test'
)

if __name__ == "__main__":
    app.run_server(port=8081, debug=True)

```
![Dash JBrowse LGV in python app](./images/python_app.png)
You can customize the Linear Genome View by modifying the `jbrowse_conf`. The `jbrowse_conf` is an instance of our `JBrowseConfig`, and can be modified to set an assembly, add tracks, set custom color palettes and more.



## Installation

### PyPI

```
$ pip install jbrowse-jupyter
```

### Install with conda

Clone this repository and [install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). Once you have conda installed, follow the steps found below 
to create a conda envirnment and install the dependecies.
```
$ cd jbrowse-jupyter
$ conda create -n myenv python=3.8
$ conda activate myenv
$ pip install -r requirements.txt
```
You can find two examples in the root of the directory. 
`browser.py` or the `browser.ipynb`

`browser.py` uses the Dash library to create a python application with the Dash JBrowse LinearGenomeView component and configured with the help of this package. `browser.ipynb` is jupyter notebook using the JupyterDash library to embed a Dash JBrowse LinearGenomeView component in a cell.

To run the Python Dash application
```
$ python browser.py
```

To run the jupyter notebook
Make sure you have jupyter notebook or jupyterlab.

Within the myenv conda environment
```
$ pip install jupyterlab
```
More information on using a specific [environment in 
a jupyter notebook](https://softwarejargon.com/jupyterlab-and-conda-environment-installation-and-setup/)


For more information about Dash and Dash applications check out these articles.

## Usage
The `jbrowse-jupyter` package provides several utility functions to create and launch Dash JBrowse components in python applications and jupyter notebooks.

* `create`(view_type, **kwargs)- creates a JBrowseConfig configuration object given a view_type 
    - view : creates a default empty JBrowseConfig. e.g `create`('view', genome='hg19')
    - conf: creates a JBrowseConfig from one of the default genomes, e.g `create`('conf')
* `create_component`(conf, **kwargs) - creates and returns a Dash JBrowse LinearGenomeView component
    - component can be used as any Dash component in Dash applications
* `launch`(conf, **kwargs) - launches a LinearGenomeView Dash component in a Jupyter cell
    > **Warning**: Only use `launch` in jupyter notebooks


### JBrowseConfig
Quick overview of the JBrowseConfig API

The JBrowseConfig API allows us to set an assembly, add tracks, set default sessions, set custom color themes, and more.

JBrowseConfig().
* `set_assembly`(assembly_data, aliases, refname_aliases)
    - Sets the assembly subconfiguration
* `add_df_track`(track_data, name, **kwargs)
    - requires DataFrame to have columns ['refName', 'start', 'end', 'name']
    - refName and name columns must be strings, start and end must be int
    - if the score column is present, it will create a Quantitative track else it will create a Feature track.
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
        * track_type (str) – (optional) track type
        * overwrite (boolean) – (optional) overwrites existing track if it exists in list of tracks (default False)
* `set_location`(location)
    - initial location for when the browser first loads, syntax 'refName:start-end' 
    - e.g 'chrom1:500-1000'
* `set_default_session`(tracks_ids, display_assembly=True)
    - sets the default session given a list of track ids
    - params:
        * tracks_ids - list[str] list of track ids to display
        * display_assembly (boolean) – display the assembly reference sequence track. default=True
* `set_theme`(primary, secondary=None, tertiary=None, quaternary=None)
    - sets the theme in the configuration given up to 4 hexadecimal colors
* `add_text_search_adapter`(ix_path, ixx_path, meta_path, adapter_id=None)
    - adds a trix text search adapter
* `get_config`() - returns the configuration object
<!-- These configurations can be used to create [Dash JBrowse's Linear Genome View](https://github.com/GMOD/dash_jbrowse) components which can be used in any python application and or jupyter notebook. -->

<!-- The JBrowseConfig API allows us to set an assembly, add tracks, set default sessions, set custom color themes, and more. -->
 <!-- For full details please reference the documentation. -->

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
    https://github.com/GMOD/dash_jbrowse/issues/new
-   Join our developers chat at https://gitter.im/GMOD/jbrowse2
-   Send an email to our mailing list at `gmod-ajax@lists.sourceforge.net`

<!-- ## FAQ
* What is an assembly and how do I configure one?
    - An assembly is
* What is a track and how do I add one to the configuration?
    - A track is
* How do I configure text searching?
    - In order to configure text searching in your Linear Genome View, you must first create a text index. Follow the steps found [here](https://jbrowse.org/jb2/docs/quickstart_cli/#indexing-feature-names-for-searching). Then you must create and add a text search adapter to your config. 
* How do I set a default session?
* How do I set a custom color theme palette to fit with my application? -->
