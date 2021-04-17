from ._bbai_capi import ffi
import pathlib

srcdir = pathlib.Path(__file__).parent.absolute()
bbai_handle = ffi.dlopen(str(srcdir / "bbai.so"))
