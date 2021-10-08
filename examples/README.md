# Examples

This directory contains examples in the form of Jupyter notebooks.
They can be run in the followings ways.

## MS Visual Studio Code Devcontainer

The `.devcontainer` folder include a configuration for automatically opening the project
in a container. For more information on enabling this behavior in VSCode, see
https://code.visualstudio.com/docs/remote/containers.

When opening the project folder in VSCode, you should get a popup asking you if you
want to open the project in a container. If not, you can hit **F1** and select
**Remote-Containers: Reopen in container**. At this point, you should be able to
open the example notebooks and they will render inline.

## Run Jupyter notebook server in Docker

The notebook server can also be run using the supplied Dockerfile. To build the
container, run the following command::

    docker build -t wasi-data-python:latest -f docker/Dockerfile .

To start the container, you run::

    docker run --rm -p 8888:8888 -p 8787:8787 -p 8786:8786 \
           -v $(pwd):/wasi-data-python -u vscode -w /wasi-data-python wasi-data-python:latest

The three ports are the notebook server, the Dask scheduler and Bokeh.  These
allow you to use the Dask dashboard in Jupyter Lab.

## Run directly on your machine

If you want to run without Docker, you can install the Python requirements locally
(preferrably in a virtual environment), install the `witxcraft` package, and
run the notebook manually.

    pip install -r examples/requirements.txt
    python setup.py install
    jupyter lab