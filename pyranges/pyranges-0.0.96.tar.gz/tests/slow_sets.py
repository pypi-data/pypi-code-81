#!/usr/bin/env python3

import pyranges as pr

f1 = "seed3821_n10000.sorted.bed"
f2 = "seed7847_n10000.sorted.bed"
b1 = pr.read_bed(f1)
b2 = pr.read_bed(f2)
b1.intersect(b2)
