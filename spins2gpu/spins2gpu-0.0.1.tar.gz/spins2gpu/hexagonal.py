#!/usr/bin/env python3

import sys, time, random
import numpy as np
from numba import cuda
from mpi4py import MPI
from spins import randomNG, hexagonal_update

#
kB = 8.61733e-2 # 玻尔兹曼常数(meV/K)

def run(X, Y, Ja, arrays_temperatures, niterations):
    comm = MPI.COMM_WORLD
    rank = comm.rank
    rank_do = comm.rank - 1 if (comm.rank - 1 >= 0) else comm.size - 1
    rank_up = comm.rank + 1 if (comm.rank + 1 < comm.size) else 0
    X_s = X // 2
    Y_s = ( Y //2 ) // comm.size
    rnu = randomNG.curandRNG(seed = 10 + 42 * rank)
    randval = cuda.device_array((Y_s, X_s), dtype=np.float32)
    latt_0 = cuda.device_array((Y_s, X_s), dtype=np.float32)
    latt_1 = cuda.device_array((Y_s, X_s), dtype=np.float32)
    latt_2 = cuda.device_array((Y_s, X_s), dtype=np.float32)
    latt_3 = cuda.device_array((Y_s, X_s), dtype=np.float32)
    threads = 128
    blocks = (X_s * Y_s + threads - 1) // threads

    rnu.Uniformint(latt_0)
    rnu.Uniformint(latt_1)
    rnu.Uniformint(latt_2)
    rnu.Uniformint(latt_3)

    ipch_0 = comm.allgather(latt_0.get_ipc_handle())
    ipch_1 = comm.allgather(latt_1.get_ipc_handle())
    ipch_2 = comm.allgather(latt_2.get_ipc_handle())
    ipch_3 = comm.allgather(latt_3.get_ipc_handle())
    lattice_0 = [x.open() if i != rank else latt_0 for i,x in enumerate(ipch_0)]
    lattice_1 = [x.open() if i != rank else latt_1 for i,x in enumerate(ipch_1)]
    lattice_2 = [x.open() if i != rank else latt_2 for i,x in enumerate(ipch_2)]
    lattice_3 = [x.open() if i != rank else latt_3 for i,x in enumerate(ipch_3)]

    f = open("hexagonal_{}_{}_{}.log".format(Y, X, Ja),'w', buffering=1)
    # Warmup iterations
    if rank == 0:
        print("Starting...",file=f)
        sys.stdout.flush()

    t0 = time.time()
    for i in range(niterations):
        hexagonal_update.update(lattice_0, lattice_1, lattice_2, lattice_3, Ja, randval, rnu, 1, rank, blocks, threads)
    t1 = time.time()
    t = t1 - t0
    
    # Compute average magnetism
    m = (np.sum(lattice_0[rank], dtype=np.int64) + np.sum(lattice_1[rank], dtype=np.int64) + np.sum(lattice_2[rank], dtype=np.int64) + np.sum(lattice_3[rank], dtype=np.int64)) / float(X * Y)
    m_global = comm.allreduce(m, MPI.SUM)
    
    if (rank == 0):
        print("{:>8}{:>12}{:>21}{:>16}{:>16}{:>16}".format("nGPUs","iterations","lattice dimensions","time(s)","reversal(ns)","magnetism"),file=f)
        print("{:>8}{:>12}{:>9} * {:<9}{:>16.6f}{:>16.6f}{:>16.6f}".format(comm.size,niterations,Y,X,t,((Y * X * niterations) / t * 1e-9),np.abs(m_global)),file=f)
        sys.stdout.flush()
    
    print("{:>16}{:>16}{:>16}".format("Temperature","magnetism","time(s)"),file=f)
    for temperature in arrays_temperatures:
        val = (1.0) / (temperature * kB)
    
        # Trial iterations
        t0 = time.time()
        for i in range(niterations):
            hexagonal_update.update(lattice_0, lattice_1, lattice_2, lattice_3, Ja, randval, rnu, val, rank, blocks, threads)

        t1 = time.time()
        t = t1 - t0
    
        # Compute average magnetism
        m =  (np.sum(lattice_0[rank], dtype=np.int64) + np.sum(lattice_1[rank], dtype=np.int64) + np.sum(lattice_2[rank], dtype=np.int64) + np.sum(lattice_3[rank], dtype=np.int64)) / float(X * Y)
        m_global = comm.allreduce(m, MPI.SUM)
        
        if (rank == 0):
            print("{:>16}{:>16.6f}{:>16.6f}".format(temperature,np.abs(m_global),t),file=f)
        sys.stdout.flush()
    f.close()
