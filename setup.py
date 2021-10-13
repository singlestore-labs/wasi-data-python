#!/usr/bin/env python3

from setuptools import setup

setup(
    name="witxcraft",
    version="0.1.0",
    author="SingleStore",
    author_email="support@singlestore.com",
    url="http://github.com/singlestore-labs/wasi-data-python",
    description="Functions for make WASM functions compatible with pandas & Dask.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    packages=['witxcraft'],
    install_requires=["pandas", "wasmtime"],
    platforms="any",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=False,
)
