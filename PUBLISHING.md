## Publishing

### Testing release in test PyPI

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
