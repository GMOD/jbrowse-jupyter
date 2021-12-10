# Contributing
We use conda environments for development.

First install conda. Read the [conda docs](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) for getting started with conda and clone the directory.

## Development
Now we can
1. after cloning the repo, cd into jbrowse-jupyter
```
$ cd jbrowse-jupyter
```
2. create a conda environment and install the dependencies
```
$ conda create -n myenv python=3.6
$ source avtivate myenv
$ python -m pip install -r requirements.txt
```
This command will create a conda environment with python 3.6. 

3. Now you are ready to run the the example
```
$ python browser.py
```
4. For development with jupyter lab or jupyter notebooks, install
jupyter lab or jupyter notebook following [these docs](https://jupyter.org/install)
More about configuring your [jupyter notebook env](https://softwarejargon.com/jupyterlab-and-conda-environment-installation-and-setup/).

5. For testing the package in another environment, you can pip install a specific branch with this command
```
$ pip install git+https://github.com/GMOD/jbrowse-jupyter.git@branch
``` 

## Running the tests and lint
You can find all the tests in the `tests/` directory
To run the tests, you can run this command from the root of the repo directory
```
$ python -m pytest tests/
```
We use flake8 for linting. You can run 
```
$ flake8 --count
```
from the root of this repo to see any lint errors

## Sphinx Docs
https://gmod.github.io/jbrowse-jupyter/
We store the docs in `docs/` directory. Our docs are created with Sphinx.
Check [this](https://www.sphinx-doc.org/en/master/contents.html) out for Sphinx documentation.
```
$ cd docs
```
You should see a requirements.txt, Makefile and a make.bat file, docs/ and source/ directories etc
1. after creating an environment, install the dependencies
```
$ conda create -n myenv python=3.6
$ source activate myenv
$ python -m pip install -r requirements.txt
```
2. Make modifications in the `source` directory
    - the main entry point for the docs is the source/index.rst
3. After making any modifications, 
```
$ make html
```
Run this command from the same place where the Makefile exists.
you can also run 
```
$ make clean
```
to delete the contentst of docs/docs directory

5. To view your changes, you can checkout `docs/docs/html/index.html`
6. When you are ready to publish any changes, make a PR against the gh-pages branch. We host our sphinx docs in github pages, and oushing to the gg-pages will publish the updated docs. Once those are published, you can check out this link to view your live docs https://gmod.github.io/jbrowse-jupyter/



## Releasing/publishing 

### Testing Pypi
1. create an account with [test PyPi](https://test.pypi.org/) and `pip install twine`

2. generate an API Token for this 'jbrowse-jupyter' package. You will need to be added as a contributor first

3. Make sure that you have update the version in your setup.py

4. From the root of the directory, run
```
$ python setup.py sdist bdist_wheel
```
This command will create a source distribution and a wheel in a temporary directory called `dist/` and `build/` at the root of the repo. You will need this when uploading to pypi.

5. Now you can check your tar works by moving the jbrowse-jupyter-<you-version>.tar.gz to your testing env and manually installing it 
```
pip installing jbrowse-jupyter-<you-version>.tar.gz
```

6 if it worked, you can 
```
$ twine upload --repository-url https://test.pypi.org/legacy/dist/*
```
This will upload to test pypi. The command will prompt you for your username. Simply enter `__token__` and paste the API token that you generated for step 2.

7. Now you can pip install your package in any env and test if it works. When you feel ready to release then you can make a pr to main. 

### Production Pypi
1. Repeat step 2 but for production [PyPi](https://pypi.org/)
2. generate an API Token for this 'jbrowse-jupyter' package. You will need to be added as a contributor first
3. Update the version on setup.py and push to main
4. Create a tag from main
5. Draft a release in github
6. Run
```
$ python setup.py sdist bdist_wheel
```
and test that you can correctly pip install your tar
`jbrowse-jupyter-<you-version>.tar.gz`
7. if it works and you are ready to release
8. Run 
```
twine upload dist/*
```
This will upload to pypi. The command will prompt you for your username. Simply enter `__token__` and paste the API token that you generated for step 2.
9. Test that it works by pip installing in a new env and running your jupyter notebook.
10. Add your tar and wheel files to your github release, and link to the new version on pypi.
11. Publish your github release.
