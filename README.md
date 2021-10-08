# wasi-data-python

This project includes Python utilities related to the
[wasi-data](https://github.com/singlestore-labs/wasi-data) specification.

## WASI

[WASI](https://wasi.dev/) is a modular system interface for WebAssembly. Checkout this [blog post](https://hacks.mozilla.org/2019/03/standardizing-wasi-a-webassembly-system-interface/) for an excellent overview and introduction. This system interface securely
and portability provides an interface to run WebAssembly modules [outside of the Web](https://webassembly.org/docs/non-web/).

## Interface types

A fantastic overview of the [interface types proposal](https://github.com/WebAssembly/interface-types/blob/master/proposals/interface-types/Explainer.md) is this [blog post](https://hacks.mozilla.org/2019/08/webassembly-interface-types/).

## Walkthrough

Currently the primary use of the package is wrapping WASM functions with
callable objects compatible with pandas and Dask DataFrame `apply` methods.
This allows you to write functions in Rust, C, Go, or any other language
that compiles to WASM, and use those functions in your DataFrame workflows.

```python
import witxcraft as wc

# Wrap all functions in a WASM module in Python wrappers.
# A WITX file in required to describe the function signatures.
# If the WITX file has the same basename as the WASM file,
# the witx= parameter does not need to be specified.
wasm_funcs = wc.fromwasmmod('mylib.wasm', witx='mylib.witx')

# Each function in the WASM file is now available as a
# callable object on the returned object. The function can be
# called standalone.
wasm_funcs.mult(10, 5)

# Or they can be used in DataFrame methods that apply functions.
df = pd.DataFrame([...], columns=['a', 'b'])
df['a'].apply(wasm_funcs.mult, args=[5])
df['a'].apply(wasm_funcs.mult, df['b'])
wasm_funcs.mult(df['a'], df['b'])
```

The [examples](examples) folder also contains examples in Jupyter notebook form.
See the [README.md](examples/README.md) file in that directory for information on how to run
them.
