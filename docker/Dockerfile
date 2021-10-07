# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT=3-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# Install examples requirements
COPY examples/requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
     	graphviz

# Install Rust and witx-bindgen
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
RUN /root/.cargo/bin/cargo install --git https://github.com/bytecodealliance/witx-bindgen witx-bindgen-cli && mv /root/.cargo/bin/witx-bindgen /usr/bin/

# Install witxcraft
COPY setup.py /tmp/pip-tmp/
COPY README.md /tmp/pip-tmp/
ADD witxcraft/ /tmp/pip-tmp/witxcraft
RUN (cd /tmp/pip-tmp && python3 setup.py install -f)

# Expose jupyter and Dask dashboard ports
EXPOSE 8787
EXPOSE 8786
EXPOSE 8888

CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
