[![Downloads](https://pepy.tech/badge/jbrowse-jupyter)](https://pepy.tech/project/jbrowse-jupyter)

# JBrowse Jupyter

JBrowse Jupyter is a python package that let's you create JBrowse 2 views in
Jupyter notebooks

## Demos

- Basic usage -
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GMOD/jbrowse-jupyter/blob/main/browser.ipynb)
- SKBR3 cancer cell line demo -
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GMOD/jbrowse-jupyter/blob/main/skbr3.ipynb)

## Tutorials

- Tutorial for setting up JupyterLab locally with jbrowse-jupyter
  https://github.com/GMOD/jbrowse-jupyter-tutorial/

## Documentation

More documentation here
https://gmod.github.io/jbrowse-jupyter/docs/html/index.html

## Installation

```
$ pip install jbrowse-jupyter
```

## Resources

- [JBrowse 2 homepage](https://jbrowse.org/jb2/)
- [Linear Genome View docs](https://jbrowse.org/storybook/lgv/main/?path=/story/getting-started--page) -
  storybook docs of React LGV
- [Dash Applications](https://dash.plotly.com/layout) how to get started to
  custumize Dash applications.
- [Dash HTML components](https://dash.plotly.com/dash-html-components) Dash html
  components to build the Dash application layout.
- [Dash JBrowse](https://github.com/GMOD/dash_jbrowse) suite of Dash components
  for JBrowse views

## Contributing

See our [contributing guide](./CONTRIBUTING.md).

## Citation

JBrowse Jupyter: a Python interface to JBrowse 2, Bioinformatics (2023)
https://doi.org/10.1093/bioinformatics/btad032

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
