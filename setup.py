#!/usr/bin/env python3
import setuptools

with open('requirements.txt') as f:
    requires = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# TODO: figure out install requires vs requirements.txt and look up classifiers
setuptools.setup(
    name="jbrowse-jupyter",
    version="0.0.2",
    author="Teresa De Jesus Martinez",
    author_email="tere486martinez@gmail.com",
    maintainer="Teresa De Jesus Martinez; JBrowse Team",
    maintainer_email="tere486martinez@gmail.com",
    description="Jupyter interface to the JBrowse's Linear Genome View",
    license="Apache-2.0",
    include_package_data=True,
    long_description=long_description,
    install_requires=requires,
    long_description_content_type="text/markdown",
    url="https://github.com/teresam856/jbrowse-jupyter",
    project_urls={
        "Bug Tracker": "https://github.com/teresam856/jbrowse-jupyter/issues",
    },
    packages=['jbrowse_jupyter'],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
)
