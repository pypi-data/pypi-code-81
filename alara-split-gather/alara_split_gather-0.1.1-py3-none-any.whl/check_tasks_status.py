#!/usr/bin/env python3
import os
import argparse

def check_status(num_tasks, sep='_', prefix='phtn_src'):
    # generate filenams for checking
    files = []
    sizes = []
    running = []
    finished = []
    for i in range(num_tasks):
        filename = os.path.join(".", f"task{i}", f"{prefix}{sep}{i}")
        files.append(filename)
        size = os.path.getsize(filename)
        sizes.append(size)
        # count running/finshed status 
        if size > 5:
            finished.append(i)
        else:
            running.append(i)

    # print the summary
    # finished tasks
    fin_str = f"{len(finished)} tasks are finished, they are:\n     "
    count = 0
    for i in finished:
        count += 1
        fin_str = f"{fin_str} {i}"
        if count>0  and count%10 == 0:
            fin_str = f"{fin_str}\n     "
    print(fin_str)
    # running tasks
    run_str = f"{len(running)} tasks are running, they are:\n     "
    count = 0
    for i in running:
        count += 1
        run_str = f"{run_str} {i}"
        if count>0 and count%10 == 0:
            run_str = f"{run_str}\n     "
    print(run_str)

   
def alara_tasks_status():
    check_tasks_status_help = ('This script check the status of alara tasks\n')
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_tasks", required=True, help="number to sub-tasks, default: 2")
    parser.add_argument("-s", "--separator", required=False, help=" '_' or '-'")
    parser.add_argument("-p", "--prefix", required=False, help="prefix of phtn_src")
    args = vars(parser.parse_args())

    # number of tasks
    if args['num_tasks'] is not None:
        num_tasks = int(args['num_tasks'])

    # prefix
    prefix = "phtn_src"
    if args['prefix'] is not None:
        prefix = args['prefix']

   # separator
    sep = '_'
    if args['separator'] is not None:
        if args['separator'] not in ['_', '-']:
            raise ValueError(f"separator {args['separator']} not supported!")
        sep = args['separator']

    check_status(num_tasks, sep=sep, prefix=prefix)
