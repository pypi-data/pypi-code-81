from distutils.core import setup, Extension

rlp = Extension('rlp',
        sources = ['aux/src/rlp.c', 'aux/src/endian.c', 'aux/src/bits.c', 'aux/src/encode.c',  'aux/src/decode.c'],
        )

setup(
        name='pylibrlp',
        version = '0.0.1a1',
        ext_modules = [rlp],
        packages=['pylibrlp'],
        )
