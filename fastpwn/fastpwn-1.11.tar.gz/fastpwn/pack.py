#!/usr/bin/env python3
from struct import pack, unpack
pk32=lambda x,endian="little",b=0:pack(">I",x+b) if endian=="big" else pack("I", x+b)
pk64=lambda y,endian="little",b=0:pack(">Q",y+b) if endian=="big" else pack("Q", y+b)
up32=lambda x,endian="little",b=0:unpack(">I",x+b)[0] if endian=="big" else unpack("I",x+b)[0]
up64=lambda y,endian="little",b=0:unpack(">Q",y+b)[0] if endian=="big" else unpack("Q",y+b)[0]
