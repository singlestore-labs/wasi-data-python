# Compiling the files in this Makefile requires clang12 as well as the libraries
# from https://github.com/WebAssembly/wasi-sdk/releases/tag/wasi-sdk-12. Note that
# the wasi-sdk files should be installed in /opt/wasi-sdk/wasi-sysroot, whereas
# libclang_rt.builtins-wasm32.a should go in /usr/lib/clang/12.0.1/lib/wasi/.

all: df.wasm

df.wasm: df.c df.h df_impl.c
	clang --target=wasm32-unknown-wasi -mmultivalue -Xclang -target-abi -Xclang experimental-mv -mexec-model=reactor --sysroot=/opt/wasi-sdk/wasi-sysroot/ -s -o df.wasm df_impl.c df.c
