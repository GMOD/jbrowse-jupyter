# Contributing

We use conda environments for development.

First install conda. Read the
[conda docs](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
for getting started with conda.

## Development

1. Clone this directory and cd into jbrowse-jupyter

```
$ cd jbrowse-jupyter
```

2. Create a conda environment and install the dependencies

```
$ conda create -n myenv
$ source activate myenv
$ python -m pip install -r requirements.txt
```

This command will create a conda env with python 3.6.

3. Now you are ready to run the the example

```
$ python browser.py
```

4. For development with jupyter lab or jupyter notebooks, install jupyter lab or
   jupyter notebook following [these docs](https://jupyter.org/install) More
   about configuring your
   [jupyter notebook env](https://softwarejargon.com/jupyterlab-and-conda-environment-installation-and-setup/).

5. You can now test the package by installing it in dev mode. This command will
   install the package in dev mode

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

6. For testing the package in another environment, you can pip install a
   specific branch with this command

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

https://gmod.github.io/jbrowse-jupyter/ We store the docs in `docs/` directory.
Our docs are created with Sphinx. Check
[this](https://www.sphinx-doc.org/en/master/contents.html) out for Sphinx
documentation.

First,

```
$ cd docs
```

You should see a requirements.txt,a Makefile, a make.bat file, the source/
directory, the docs/ directory which stores the build etc.

1. Create an environment and install the dependencies.

```
$ conda create -n myenv
$ source activate myenv
$ python -m pip install -r requirements.txt
```

2. Now you are ready to make modifications. Make any modifications to the docs
   in the `source` directory
   - the main entry point for the docs is the source/index.rst
3. After making any modifications,

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
directory stores the actualy configuration and contents of the sphinx docs.

5. To view your changes, you can checkout `docs/docs/html/index.html`
6. When you are ready to publish any changes, make a PR against the gh-pages
   branch. We host our sphinx docs in github pages, and pushing to the gh-pages
   will publish the updated docs. Once those are published, you can check out
   this link to view your live docs https://gmod.github.io/jbrowse-jupyter/

## Releasing/publishing

### Testing release in test Pypi

1. Create an account with [test PyPi](https://test.pypi.org/) and
   `pip install twine`

2. Generate an API Token for the 'jbrowse-jupyter' package. You will need to be
   added as a contributor first

3. Make sure that you have updated the version in your setup.py

4. From the root of the directory, run

```
$ python setup.py sdist bdist_wheel
```

This command will create a source distribution and a wheel in a temporary
directory called `dist/` and `build/` at the root of the repo. You will need
this when uploading to pypi.

5. Now you can check your tar works by moving the
   jbrowse-jupyter-<you-version>.tar.gz to your testing env and manually
   installing it

```
pip installing jbrowse-jupyter-<your-version>.tar.gz
```

6 if it worked, you can run

```
$ twine upload --repository-url https://test.pypi.org/legacy/dist/*
```

This will upload the contents of your dist folder to test pypi. The command will
prompt you for your username. Simply enter `__token__` and paste the API token
that you generated in step 2.

7. Now you can pip install your package in any env and test that it works. When
   you feel ready to release then you can make a pr to main.

### Production Pypi

1. Repeat step 2 but for production [PyPi](https://pypi.org/)
2. Generate an API Token for the 'jbrowse-jupyter' package. You will need to be
   added as a contributor first.
3. Update the version on setup.py and when you are ready push to main.
4. Create a tag from main
5. Draft a release in github
6. Checkout the github tag and from the tag, run

```
$ python setup.py sdist bdist_wheel
```

from the root of the github directory. Test that you can correctly pip install
your tar `jbrowse-jupyter-<you-version>.tar.gz` 7. If it works and you are ready
to release, run

```
twine upload dist/*
```

This will upload to pypi. The command will prompt you for your username. Simply
enter `__token__` and paste the API token that you generated for step 2. 8. Test
that it works by pip installing in a new env and running the python app. 10. Add
your tar and wheel files to your github release, and link to the new version on
pypi. 11. Publish the github release.

## Maintenance

This package depends on `Dash JBrowse`. The repo can be found
[here](https://github.com/GMOD/dash_jbrowse). The [Dash JBrowse] package
currently has a dependency on the JBrowse React Linear Genome View npm package.
In order to keep up with the dependencies, the version of the Browse React
Linear Genome View npm package was set up to allow newer versions. If there are
any breaking changes, we will need to update the version in Dash JBrowse

1. Checkout the
   [dash_jbrowse](https://github.com/GMOD/dash_jbrowse/blob/main/CONTRIBUTING.md)
   repo
2. install the dependencies with npm
3. Update the
   [JBrowse React Linear Genome View npm package](https://www.npmjs.com/package/@jbrowse/react-linear-genome-view)
4. Make sure the package.json was updated with the latest version of the React
   Linear Genome View package
5. Test everything works appropriately by running

```
$ npm run build
$ python usage.py
```

Verify the app works appropriately Run the tests and make a pr to main. We can
draft a release following the contributing docs found
[here](https://github.com/GMOD/dash_jbrowse/blob/main/CONTRIBUTING.md)

6. Now you can update this package and upgrade the python dash-jbrowse package
   dependency to the latest version of dash jbrowse.
7. Follow the release steps mentioned above for jupyter jbrowse
8. Test that everything works as expected, and you are done!
