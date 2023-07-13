## Publishing

General publishing involves creating a new tag

```bash
# e.g.
git tag v1.2.3
git push --tags
```

And then going to https://github.com/GMOD/jbrowse-jupyter/tags and doing "create
release" from the new tag. Then a github action will automatically create the
tags

The below is just for when you don't want to use the github actions process

### Testing release in test PyPI without github action

1. Create an account with [test PyPI](https://test.pypi.org/) and
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
   you feel ready to release then you can make a PR to main.

### Production PyPI

1. Repeat step 2 but for production [PyPI](https://pypi.org/)
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
pypi.

11. Publish the github release.
