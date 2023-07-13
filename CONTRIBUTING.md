# Contributing

We use conda environments for development.

First install conda. Read the
[conda docs](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
for getting started with conda.

## Development

### Clone this directory and cd into jbrowse-jupyter

```
$ cd jbrowse-jupyter
```

### Create a conda environment and install the dependencies

```
$ conda create -n myenv
$ source activate myenv
$ python -m pip install -r requirements.txt
```

This command will create a conda env with python 3.6.

### Run the the example

```
$ python browser.py
```

### For development with jupyter lab or jupyter notebooks

Install jupyter lab or jupyter notebook following
[these docs](https://jupyter.org/install) More about configuring your
[jupyter notebook env](https://softwarejargon.com/jupyterlab-and-conda-environment-installation-and-setup/).

### Test package in dev mode

```
$ python -m pip install -e .
```

To verify that the package was installed, you can run

```
$ pip list
```

This will display the list of packages in your conda env. Look for the
`jbrowse-jupyter` package.

You can read more about working in
[development mode here](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#working-in-development-mode).

### Testing the package in other environments

You can pip install a specific branch with this command

```
$ pip install git+https://github.com/GMOD/jbrowse-jupyter.git@branch
```

## Lint and Tests

You can find all the tests in the `tests/` directory To run the tests, you can
run this command from the root of the repo directory

```
$ pip install pytest
$ python -m pytest tests/
```

We use flake8 for linting. You can run

```
$ pip install flake8
$ flake8 --count
```

from the root of this repo to see any lint errors

## Sphinx Docs

https://gmod.github.io/jbrowse-jupyter/

We store the docs in `docs/` directory. Our docs are created with Sphinx. Check
[this](https://www.sphinx-doc.org/en/master/contents.html) out for Sphinx
documentation.

### Generate docs

```
$ cd docs
```

You should see a requirements.txt,a Makefile, a make.bat file, the source/
directory, the docs/ directory which stores the build etc.

### Create an environment and install the dependencies.

```
$ conda create -n myenv
$ source activate myenv
$ python -m pip install -r requirements.txt
```

### Make any modifications to the docs in the `source` directory

The main entry point for the docs is the source/index.rst After making any
modifications,

```
$ make clean
```

to delete the contents of docs/docs directory

Now you can run

```
$ make html
```

The command above will create a build of the docs and stores them in a
subdurectory called docs. For configuring the docs check out the conf.py in the
source/ directory. For configuration of the builds, checkout the docs/Makefile
and docs/make.bat files.

**_Note:_** there parent docs directory stores all the docs. The docs child
directory stores the build of the docs when running make html. The source child
directory stores the actually configuration and contents of the sphinx docs.

## View your changes at `docs/docs/html/index.html`

## Publish docs by making a PR against the gh-pages

We host our sphinx docs in github pages, and pushing to the gh-pages will
publish the updated docs. Once those are published, you can check out this link
to view your live docs https://gmod.github.io/jbrowse-jupyter/
