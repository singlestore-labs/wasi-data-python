#!/usr/bin/env python3

"""
The WITXCraft package is a collection of utilites for working with WITX.
WITX is a file format for describing WASI APIs using types not available
in native WASM.

https://github.com/WebAssembly/WASI/blob/main/docs/witx.md

"""

__version__ = "0.1.0"

from .ufunc import fromwasmmod
from .parse import parse_witx
