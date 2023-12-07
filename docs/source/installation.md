## Installation

### PyPI

```
$ pip install jbrowse-jupyter
```

### Install with conda

Clone the GMOD/jbrowse-jupyter
[repository](https://github.com/GMOD/jbrowse-jupyter) and
[install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).
Once you have conda installed, follow the steps found below to create a conda
environment and install the dependencies.

```
$ cd jbrowse-jupyter
$ conda create -n myenv
$ conda activate myenv
$ pip install -r requirements.txt
```

You can find examples in the root of the directory.

- LGV - `browser.py` or the `browser.ipynb`
- CGV - `cgv_examples.py` or `cgv_examples.ipynb`

`browser.py` uses the Dash library to create a python application with the Dash
JBrowse LinearGenomeView component and configured with the help of this package.
`browser.ipynb` is jupyter notebook using the Dash library to embed a Dash
JBrowse LinearGenomeView component in a cell. `cgv_examples.py` a Dash
application using the Dash JBrowse CircularGenomeView component
`cgv_examples.ipynb` is jupyter notebook using the Dash library to embed a Dash
JBrowse CircularGenomeView component in a cell.

To run the Python Dash application

```
$ python browser.py
```

To run the jupyter notebook Make sure you have jupyter notebook or jupyterlab.

Within the myenv conda environment

```
$ pip install jupyterlab
```

More information on using a specific
[environment in a jupyter notebook](https://softwarejargon.com/jupyterlab-and-conda-environment-installation-and-setup/)

For more information about Dash and Dash applications check out these articles.

### Resources

- [Dash Applications](https://dash.plotly.com/layout) how to get started to
  custumize Dash applications.
- [Dash HTML components](https://dash.plotly.com/dash-html-components) Dash html
  components to build the Dash application layout.
- [DashJupyter](https://github.com/plotly/jupyter-dash) library to enable
  embedding Dash components in jupyter notebooks.
- [DashJbrowse](https://github.com/GMOD/dash_jbrowse) suite of Dash components
  for JBrowse views. (JBrowse Linear Genome View and JBrowse Circular Genome
  View)
- [JBrowse Docs](https://jbrowse.org/jb2/)
- [JBrowse Config Guide](https://jbrowse.org/jb2/docs/config_guide/)
- [JBrowse Views](https://jbrowse.org/jb2/download/#embedded-components)
