## Local file support
We currently support two ways of passing your local data to JBrowse Views.

For our **Jupyter lab and Jupyter notebook** users, you can create urls by leveraging the Jupyter server where your notebook is running or you can provide paths relative to root of the file tree. You can also provide paths relative to the root of the Jupyter file tree. Examples of these can be found below or in the
local_support.ipynb.

For those using **colab notebooks and binder** (will also work in Jupyter) you can use the JBrowse dev server. An example of how to use the JBrowse dev server can be found below.

> **Note**: These solutions are recommended for your development environments and not supported in production.

A tutorial can be found in the root of the directory named [local_support.ipynb](https://github.com/GMOD/jbrowse-jupyter/blob/main/local_support.ipynb)
### Jupyter Server

Jupyter Lab and Jupyter Notebook users can leverage the Jupyter server to create urls or paths to pass to JBrowse Jupyter view configs. 

Once you have the data within the file tree where the notebook is running, then you will be able to format the urls or paths to pass to the API. (Note: you will need to serve your entire project where the notebook is running.)

To verify that your data is in the correct place, you can navigate to *http://your-host:your-port/tree* . Make sure that you use the same port and host that is used in your jupyter configuration. 

e.g http://localhost:8888/tree is the url your should navigate to if you are running your jupyter notebook in localhost in port 8888

If you have a different port or host, you can change the port and host used by JBrowse with the use of the set_env(notebook_host, notebook_port). 

Example:
config = create("LGV)
config.set_env("host", 9999).

#### Using Jupyter URLS

In this example, the notebook is configured to run in localhost in port 8888. It is assumed that you have Jupyter lab installed in your venv.

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

This will be the url that you should see at the top of your browser if you opened the example.ipynb
http://localhost:8888/lab/tree/example.ipynb

Urls for file `data1.gff.gz` and `data2.gff.gz.tbi`
would be in the form `http://localhost:8888/files/<your_file_name>`.
* `http://localhost:8888/files/data1.gff.gz`
* `http://localhost:8888/files/data2.gff.gz.tbi`
Note that you do not need to add lab or tree to this url.

You can use these urls. For example, you could add a track with thse urls like this:
```python

config.add_track(
    "http://localhost:8888/files/data1.gff.gz", # track data
    index="http://localhost:8888/files/data2.gff.gz.tbi", # track index
    track_id="example-track", # track id
    name="track-name" # track name
)
```

Resources:
* [Configuring the Jupyter Notebook server](https://jupyter-notebook.readthedocs.io/en/stable/config_overview.html#notebook-server)
* [Getting started with Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/getting_started/starting.html)

#### Using Jupyter paths
JBrowse also supports paths to files are within the Jupyter file tree (this only works if you are running your notebook in Jupyter lab or Jupyter notebook).

You can repeat the steps in the previous section to ensure that your files are in the correct place. Instead of formatting the urls yourself, you can pass paths **relative to the root of the Jupyter file tree** .

Using the same structure of the previous example...

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
A user could then specify paths to data1 and data2 like this
```python

config.add_track(
    "/data1.gff.gz", # track data
    index="/data2.gff.gz.tbi", # track index
    track_id="example-track", # track id
    name="track-name" # track name
)
```

### JBrowse dev server
We also provide a simple http server configured with CORS that will allow you to serve your local files from a specified directory within your machine.

> **Note** The use of local files or the dev server provided is not recommended for production environments. 

You can spin the dev server in two ways.
1. Git clone this repo
2. From the root of this repository, you will be able to run the python file named `serve.py`
```$ python serve.py```
3. You can choose your own port, host, and directory from which to serve your files. You can also press enter to choose all the defaults. 
  - Default PORT: 8080
  - Default host: localhost
  - Default directory: the current working directory -> os.getcwd() is used

4. Now that the dev server is running you can use the url provided in the terminal to pass to your views. 
- For example: the url to the data you wish to pass to the JBrowse view config for the local dev server running on port 8080 on local host will look like this "http://localhost:8080/<your-file-name>"
e.g `jbrowse_conf.add_track("http://localhost:8080/<your-file-name>", name="test-demo")`

Or you can make your own python file and run it to start the server.

1. create a python file named dev_server.py and add the code below

```
import os
from jbrowse_jupyter import serve


if __name__ == "__main__":
    serve(os.getcwd(), port=8080, host='localhost')
```
2. Run the python file
`$ python dev_server.py`

3. This will spin up a python simple http server with cors enabled. You can take a look at our implementation of our dev server here: `jbrowse_jupyter/dev_server.py`

4. Now that the dev server is running you can use the url provided in the terminal to pass to your views. 
- For example: the url to the data you wish to pass to the JBrowse view config for the local dev server running on port 8080 on local host will look like this "http://localhost:8080/<your-file-name>"
e.g `jbrowse_conf.add_track("http://localhost:8080/<your-file-name>", name="test-demo")`
