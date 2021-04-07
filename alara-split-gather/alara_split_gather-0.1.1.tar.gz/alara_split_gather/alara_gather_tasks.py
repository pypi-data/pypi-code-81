#!/usr/bin/env python3
import numpy as np
import tables as tb
import os
import argparse
from pyne.alara import _make_response_dtype

def append_photon_source_to_hdf5(num_tasks=2, nucs='all', chunkshape=(10000,),
        output='phtn_src.h5',sep='_'):
    """Converts a plaintext photon source file to an HDF5 version for
    quick later use.

    This function produces a single HDF5 file named <filename>.h5 containing the
    table headings:

        idx : int
            The volume element index assuming the volume elements appear in xyz
            order (z changing fastest) within the photon source file in the case of
            a structured mesh or mesh.mesh_iterate() order for an unstructured mesh.
        nuc : str
            The nuclide name as it appears in the photon source file.
        time : str
            The decay time as it appears in the photon source file.
        phtn_src : 1D array of floats
            Contains the photon source density for each energy group.

    Parameters
    ----------
    nucs : str
        Nuclides need to write into h5 file. For example:
            - 'all': default value. Write the information of all nuclides to h5.
            - 'total': used for r2s. Only write TOTAL value to h5.
    num_tasks : int
        Number of alara tasks.
    chunkshape : tuple of int
        A 1D tuple of the HDF5 chunkshape.
    """
    # create a hdf5 file
    phtn_dtype = _make_response_dtype('phtn_src', data_length=24)
    filters = tb.Filters(complevel=1, complib='zlib')
    h5f = tb.open_file(output, 'w', filters=filters)
    tab = h5f.create_table('/', 'data', phtn_dtype, chunkshape=chunkshape)

    # read phtn_src
    chunksize = chunkshape[0]
    rows = np.empty(chunksize, dtype=phtn_dtype)
    idx = 0
    old = ""
    row_count = 0
    files = []
    # get phtn_src files
    print(f"{num_tasks} files to be write into {output}")
    for i in range(num_tasks):
        filename = os.path.join(".", f"task{i}", f"phtn_src{sep}{i}")
        files.append(filename)
    for filename in files:
        print(f"    running with file {filename}, [{i}/{num_tasks}]")
        f = open(filename, 'r')
        for i, line in enumerate(f, 1):
            tokens = line.strip().split('\t')
            # Keep track of the idx by delimiting by the last TOTAL line in a
            # volume element.
            if tokens[0] != u'TOTAL' and old == u'TOTAL':
                idx +=1
            if nucs.lower() == 'all':
                row_count += 1
                j = (row_count-1)%chunksize
                rows[j] = (idx, tokens[0].strip(), tokens[1].strip(),
                    np.array(tokens[2:], dtype=np.float64))
            elif nucs.lower() == 'total':
                if tokens[0] == 'TOTAL':
                    row_count += 1
                    j = (row_count-1)%chunksize
                    rows[j] = (idx, tokens[0].strip(), tokens[1].strip(),
                        np.array(tokens[2:], dtype=np.float64))
            else:
                h5f.close()
                f.close()
                raise ValueError(u"Nucs option {0} not support!".format(nucs))

            # Save the nuclide in order to keep track of idx
            old = tokens[0]
            if (row_count>0) and (row_count%chunksize == 0):
                tab.append(rows)
                rows = np.empty(chunksize, dtype=phtn_dtype)
                row_count = 0
        f.close()

    if row_count % chunksize != 0:
        tab.append(rows[:j+1])
    h5f.close()
    print("Done")

def merge_phtn_src(num_tasks=2, prefix="phtn_src", output="phtn_src", sep='_'):
    """
    Merge phtn_src of sub-tasks into a single phtn_src.
    """
    print(f"{num_tasks} files to merge.")
    # get phtn_src files
    files = []
    for i in range(num_tasks):
        filename = os.path.join(".", f"task{i}", f"{prefix}{sep}{i}")
        files.append(filename)
    # write content
    fo = open(output, 'w')
    for i, filename in enumerate(files):
        print(f"    merging {filename}, [{i}/{num_tasks}]")
        with open(filename, 'r') as fin:
            cnt = fin.read()
            fo.write(cnt)
    fo.close()

def alara_gather_tasks()
    gather_alara_task_help = ('This script gather alara output and phtn_src\n')
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_tasks", required=False, help="number to sub-tasks, default: 2")
    parser.add_argument("-m", "--mode",required=False, help="mode of gather, txt or h5")
    parser.add_argument("-o", "--output", required=False, help="output file")
    parser.add_argument("-p", "--prefix", required=False, help="prefix of alara output")
    parser.add_argument("-s", "--separator", required=False, help=" '_' or '-'")
    args = vars(parser.parse_args())


    # number of tasks
    num_tasks = 2
    if args['num_tasks'] is not None:
        num_tasks = int(args['num_tasks'])
    print(f"num_tasks: {num_tasks}")
    
    # mode
    mode = 'h5'
    if args['mode'] is not None:
        mode = args['mode']
    print(f"mode: {mode}")
    
    # output
    if mode == 'h5':
        output = 'phtn_src.h5'
    elif mode == 'txt':
        output = 'phtn_src'
    if args['output'] is not None:
        output = args['output']
    print(f"output: {output}")
    
    # input
    prefix = "phtn_src"
    if args['prefix'] is not None:
        prefix = args['prefix']
    print(f"prefix: {prefix}")

    # separator
    sep = '_'
    if args['separator'] is not None:
        if args['separator'] not in ['_', '-']:
            raise ValueError(f"separator {args['separator']} not supported!")
        sep = args['separator']
    print(f"separator: {sep}")


    if mode == 'h5':
        append_photon_source_to_hdf5(num_tasks=num_tasks, nucs='TOTAL',
            output=output, sep=sep)
    elif mode == 'txt':
        merge_phtn_src(num_tasks=num_tasks, prefix=prefix, output=output, sep=sep)
    else:
        raise ValueError("Wrong mode")

