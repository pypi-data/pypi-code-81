#!/usr/bin/env python3

import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--model", '-m', default="ising", help="模型")
parser.add_argument("--configuration", '-c', default="hexagonal", help="结构特征")
parser.add_argument("--lattice-n", '-y', type=int, default=1024, help="模拟格子行数")
parser.add_argument("--lattice-m", '-x', type=int, default=1024, help="模拟格子列数")
parser.add_argument("--parameters", '-p', type=float, default=[3.0], nargs='+', help="磁交换关联参数(meV)")
parser.add_argument("--mae", '-a', type=float, default=[1.01], nargs='+', help="磁各向异性")
parser.add_argument("--iterations", '-i', type=int, default=1000, help="每次迭代步数")
parser.add_argument("--temperatures", '-t', type=float, default=[1, 210, 5], nargs='*', help="迭代温度区间")
args = parser.parse_args()

X = args.lattice_m
Y = args.lattice_n

i = len(args.temperatures) // 3
args.temperatures = args.temperatures[:i * 3]
arrays_temperatures = np.arange(args.temperatures[0], args.temperatures[1], args.temperatures[2])
j = 1
while j < i:
    arrays_temperatures=np.concatenate((arrays_temperatures, np.arange(args.temperatures[j * 3], args.temperatures[j * 3 + 1], args.temperatures[j * 3 + 2])))
    j += 1
niterations = args.iterations

if args.configuration == "hexagonal":
    import hexagonal
    Ja = args.parameters[0]
    hexagonal.run(X, Y, Ja, arrays_temperatures, niterations)

