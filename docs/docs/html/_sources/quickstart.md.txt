## Quickstart

JBrowse Jupyter is a python package that provides a python interface to JBrowse 2 views.

The package provides a JBrowseConfig API to facilitate the customization of JBrowse 2 React Linear Genome View's state configuration objects. It also provides utility functions to create Dash JBrowse components to embed in Dash applications and others to embed them in jupyter notebooks.

First,

install the jupyter-jbrowse package
```
$ pip install jupyter-jbrowse
```
### Jupyter Notebook

Using the package, we can create a Dash JBrowse LinearGenomeView  to embed in a jupyter cell.

1. Import the package's `create` and `launch` methods.
2. Use the `create(view_type, **kwargs)` to create a `JBrowseConfig` from one of the provided default assemblies/genomes. Currently providing hg38 and hg19. For more information about the default, you can checkout the data directory in our repo [here](https://github.com/GMOD/jbrowse-jupyter/tree/doc_updates/jbrowse_jupyter/data)
    - for further customization of the config, check functions that the JBrowseConfig provides
3. Use the `launch` utility function with the hg38 config to create and launch a Dash JBrowse Linear Genome View in a jupyter notebook cell.


![Launching hg38 LGV in python notebook](./images/quickstart.png)
*Launching a Linear Genome View in Jupyter Notebook*


![Launching hg19 CGV in python notebook](./images/quickstart2.png)
*Launching a Circular Genome View in Jupyter Notebook*
### Python Dash Application

1. Import the package's `create` and  `create_component`
2. Use the `create(view_type, **kwargs)` to create a `JBrowseConfig` from one of the provided default assemblies/genomes. Currently providing hg38 and hg19. For more information about the default, you can checkout the data directory in our repo [here](https://github.com/GMOD/jbrowse-jupyter/tree/doc_updates/jbrowse_jupyter/data)
    - for further customization of the config, check functions that the JBrowseConfig provides
3. Use `create_component` to create a Dash JBrowse Linear Genome View component. The example below uses dash and dash_html_components to create a python application.

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
![Launching hg38 LGV in python dash app](./images/python_app_conf.png)
*Launching a Linear Genome View in python Dash application*
