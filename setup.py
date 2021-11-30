import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# TODO: figure out install requires vs requirements.txt and look up classifiers
setuptools.setup(
    name="jbrowse-jupyter",
    version="0.0.1",
    author="Teresa De Jesus Martinez",
    author_email="tere486martinez@gmail.com",
    description="Jupyter and python interface to the JBrowse2 Linear Genome View",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teresam856/jbrowse-jupyter",
    project_urls={
        "Bug Tracker": "https://github.com/teresam856/jbrowse-jupyter/issues",
    },
    packages=setuptools.find_packages(exclude['tests*']),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
    ],
)
