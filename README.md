![Pytest and flake8](https://github.com/GMOD/jbrowse-jupyter/actions/workflows/push.yml/badge.svg)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/GMOD/jbrowse-jupyter/binder_updates?labpath=binder%2Fbinder.ipynb)
[![Downloads](https://pepy.tech/badge/jbrowse-jupyter)](https://pepy.tech/project/jbrowse-jupyter)

# [JBrowse Jupyter](https://gmod.github.io/jbrowse-jupyter/)

JBrowse Jupyter is a python package that let's you create JBrowse 2 views in Jupyter notebooks


![demo-gif](https://user-images.githubusercontent.com/45598764/144863573-2bcd982b-1d18-4dc8-aa2f-fd8adf4985a2.gif)

_You can open this browser.ipynb in colab_
[here](https://colab.research.google.com/github/GMOD/jbrowse-jupyter/blob/main/browser.ipynb)

## Demos

- Basic usage - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GMOD/jbrowse-jupyter/blob/main/browser.ipynb)
- SKBR3 cancer cell line demo - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GMOD/jbrowse-jupyter/blob/main/skbr3.ipynb

## Documentation

More documentation here https://gmod.github.io/jbrowse-jupyter/docs/html/index.html

## Installation


```
$ pip install jbrowse-jupyter
```



#### Using Jupyter URLS

In this example, the notebook is configured to run in localhost in port 8888. It
is assumed that you have Jupyter lab installed in your venv.

File tree of the project:

```
- example_dir/
    - example.ipynb
    - data1.gff.gz
    - data2.gff.gz.tbi
```

Running Jupyter

```
(venv)$ cd example_dir
(venv)$ jupyter lab
```

This will be the url that you should see at the top of your browser if you
opened the example.ipynb http://localhost:8888/lab/tree/example.ipynb

Urls for file `data1.gff.gz` and `data2.gff.gz.tbi` would be in the form
`http://localhost:8888/files/<your_file_name>`.

- `http://localhost:8888/files/data1.gff.gz`
- `http://localhost:8888/files/data2.gff.gz.tbi` Note that you do not need to
  add lab or tree to this url.

You can use these urls. For example, you could add a track with these urls like
this:

```python

config.add_track(
    "http://localhost:8888/files/data1.gff.gz", # track data
    index="http://localhost:8888/files/data2.gff.gz.tbi", # track index
    track_id="example-track", # track id
    name="track-name" # track name
)
```

Resources:

- [Configuring the Jupyter Notebook server](https://jupyter-notebook.readthedocs.io/en/stable/config_overview.html#notebook-server)
- [Getting started with Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/getting_started/starting.html)

## Resources

- [JBrowse](https://jbrowse.org/jb2/) - the next generation genome browser
- [JBrowse React Linear Genome View](https://www.npmjs.com/package/@jbrowse/react-linear-genome-view) -
  interactive genome browser
- [JBrowse React Linear Genome View Docs](https://jbrowse.org/storybook/lgv/main/?path=/story/getting-started--page) -
  storybook docs of React LGV
- [Dash Applications](https://dash.plotly.com/layout) how to get started to
  custumize Dash applications.
- [Dash HTML components](https://dash.plotly.com/dash-html-components) Dash html
  components to build the Dash application layout.
- [Dash Jupyter](https://github.com/plotly/jupyter-dash) library to enable
  embedding Dash components in jupyter notebooks.
- [Dash Jbrowse](https://github.com/GMOD/dash_jbrowse) suite of Dash components
  for JBrowse views. (JBrowse Linear Genome View)

## Contributing

See our [contributing guide](./CONTRIBUTING.md).

## Academic Use

This package was written with funding from the [NHGRI](https://genome.gov/) as
part of the JBrowse project. If you use it in an academic project that you
publish, please cite the most recent JBrowse paper, which will be linked from
[jbrowse.org](https://jbrowse.org/).

## Contact us


- Report a bug or request a feature at
  https://github.com/GMOD/jbrowse-jupyter/issues
- Join our developers chat at https://gitter.im/GMOD/jbrowse2
- Send an email to our mailing list at `gmod-ajax@lists.sourceforge.net`

## FAQ

### What file types are supported?

We currently support:

- bam/cram
- bigwig
- bigbed
- indexed fasta
- bgzip indexed fasta
- gff3 tabix
- twobit
- vcf
- vcf tabix

### How do I configure text searching?

In order to configure text searching in your Linear Genome View, you must first
create a text index. Follow the steps found
[here](https://jbrowse.org/jb2/docs/quickstart_cli/#indexing-feature-names-for-searching).
Then you must create and add a text search adapter to your config.

### Can I use local files/my own data?

Yes, there are a couple of ways in which you can configure and use your own data
from your local environment in jbrowse views. 1. Make use of the jupyter
notebook/lab server. Intended for those running their notebooks with jupyter lab
or jupyter notebook. 2. Launch your own http server with CORS which will enable
you to use local files. You can run our serve.py to launch our dev server.
(Checkout our local_support.ipynb for tutorials on how to use your own data)


### My data says it's is loading and never loads?

If your view shows that it is loading and never loads, it could be a fetch error
or CORS. - the JBrowse Dev Server has CORS enabled.

- Make sure that your alias is correctly configured. Data that never loads could
  also indicate that the format is correct, but will not display anything for it
  if the assembly does not match.
- Data that never loads could also indicate that the port and host do not match
  where your data is hosted when using paths in jupyter envs
