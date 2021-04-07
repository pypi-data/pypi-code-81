#!/usr/bin/env python3
import re
import os
import argparse
from alara_split_gather.utils import assign_subtasks

def is_volume_start(line):
    volume_start_pattern = re.compile("^volume", re.IGNORECASE) 
    if re.match(volume_start_pattern, line):
        return True
    else:
        return False 
def is_end(line):
    end_pattern = re.compile("^end", re.IGNORECASE)
    if re.match(end_pattern, line):
        return True
    else:
        return False

def is_mat_loading(line):
    mat_loading_pattern = re.compile("^mat_loading")
    if re.match(mat_loading_pattern, line):
        return True
    else:
        return False

def count_vols(inp="alara_inp"):
    """Count the number of vols"""
    count = 0
    with open(inp, 'r') as fin:
        vol_start = False
        while True:
            line = fin.readline()
            if not line:
                break
            if is_volume_start(line):
                vol_start = True
            if vol_start and (not is_end(line)) and (not is_volume_start(line)):
                count += 1
            if vol_start and is_end(line):
                return count

def get_zones_vols(inp="alara_inp"):
    zones, vols = [], []
    with open(inp, 'r') as fin:
        vol_start = False
        while True:
            line = fin.readline()
            if not line:
                break
            if is_volume_start(line):
                vol_start = True
            if vol_start and (not is_end(line)) and (not is_volume_start(line)):
                line_ele = line.strip().split()
                vols.append(line_ele[0])
                zones.append(line_ele[1])
            if is_end(line) and vol_start:
                break
    return zones, vols

def get_mats(inp="alara_inp"):
    mats = []
    with open(inp, 'r') as fin:
        mat_loading_start = False
        while True:
            line = fin.readline()
            if not line:
                break
            if is_mat_loading(line):
                mat_loading_start = True
            if mat_loading_start and (not is_mat_loading(line)) and (not is_end(line)):
                line_ele = line.strip().split()
                mats.append(line_ele[1])
            if mat_loading_start and is_end(line):
                break
    return mats

def split_alara_inp(inp="alara_inp", num_tasks=10, sep='_', truncation=None):
    """Split alara_inp into num_tasks sub-tasks"""
    num_vols = count_vols(inp)
    if num_vols < num_tasks:
        raise ValueError(f"num_tasks must be smaller than {num_vols}")
    zones, vols = get_zones_vols(inp)
    mats = get_mats(inp)
    #print(zones, vols, mats)
    vol_per_task = num_vols // num_tasks
    subtasks = assign_subtasks(num_vols, num_tasks)
    for tid in range(len(subtasks)):
        print(f"write files for task {tid}")
        inp_name = f"{inp}{sep}{tid}"
        fin = open(inp, 'r')
        fo = open(inp_name, 'w')
        #lines = fin.readlines()
        vol_start, vol_end = False, False
        mat_start, mat_end = False, False
        vol_write, mat_write = False, False
        while True:
            line = fin.readline()
            if ("" == line):
                break
            if is_volume_start(line):
                vol_start = True
                fo.write(line)
                continue
            if (not vol_start):
                fo.write(line)
            if vol_start and (not vol_end) and (not vol_write):
                # write specific vols
                #for i in range(vol_per_task):
                for i, item in enumerate(subtasks[tid]):
                    vid = tid*vol_per_task + i
                    cnt = f"\t {vols[vid]} {zones[vid]}\n"
                    fo.write(cnt)
                vol_write = True
                continue
            if is_end(line) and vol_start:
                vol_end = True
            if is_mat_loading(line):
                mat_start = True
                fo.write(line)
                continue
            if vol_end and not mat_start:
                fo.write(line)
            if mat_start and (not mat_end) and (not mat_write):
                # write specific mats
                #for i in range(vol_per_task):
                for i, item in enumerate(subtasks[tid]):
                    vid = tid*vol_per_task + i
                    cnt = f"\t {zones[vid]} {mats[vid]}\n"
                    fo.write(cnt)
                mat_write = True
                continue
            if mat_start and is_end(line):
                mat_end = True
            # mixture part
            if "mixture" in line:
                #import pdb; pdb.set_trace()
                line_ele = line.strip().split()
                if line_ele[1] in mats[tid*vol_per_task:tid*vol_per_task+len(subtasks[tid])]:
                    fo.write(line)
                    while True:
                        line = fin.readline()
                        if "end" in line:
                            fo.write(line)
                            break
                        else:
                            fo.write(line)
                else:
                    while True: # skip these lines
                        line = fin.readline()
                        if "end" in line:
                            line = fin.readline()
                            break
                continue
            if "phtn_src" in line:
                line_ele = line.strip().split()
                phtn_str = "     "
                for i in range(len(line_ele)):
                    if "phtn_src" in line_ele[i]:
                        line_ele[i] = f"{line_ele[i]}{sep}{tid}"
                    phtn_str = f"{phtn_str} {line_ele[i]}"
                fo.write(phtn_str)
                fo.write("\n")
                continue
            if "alara_fluxin" in line:
                #ctn = line.replace("alara_fluxin", f"alara_fluxin{tid}")
                line_ele = line.strip().split()
                skip = int(line_ele[4])
                skip += tid*vol_per_task
                #ctn = line.replace(" 0 ", f" {skip}")
                ctn = f"{line_ele[0]} {line_ele[1]} {line_ele[2]} {line_ele[3]} {skip} default"
                fo.write(ctn)
                fo.write("\n")
                continue
            if "truncation" in line and truncation is not None:
                line_ele = line.strip().split()
                ctn = f"{line_ele[0]} {truncation}\n"
                fo.write(ctn)
                continue
            if mat_end:
                fo.write(line)
        fo.close()
        fin.close()

def pbs_generation(tid, inp="alara_inp", sep='_'):
    """Generate a pbs file for current task id"""
    fo = open(f"alara_task{sep}{tid}.pbs", 'w')
    fo.write("#!/bin/bash\n")
    fo.write(f"#PSB -N task{sep}{tid}\n")
    fo.write("#PBS -l nodes=1:ppn=28\n")
    fo.write("cd $PBS_O_WORKDIR\n")
    fo.write(f"$HOME/opt/ALARA/bin/alara {inp}{sep}{tid} > output{sep}{tid}.txt\n")
    fo.close()

def alara_split_task():
    """
    Split the alara task
    """
    split_alara_task_help = ('This script read an alara_inp and split it into samller task\n')
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_tasks", required=False, help="number to sub-tasks, default: 2")
    parser.add_argument("-i", "--input", required=False, help="ALARA input, default: alara_inp")
    parser.add_argument("-d", "--data", required=False, help="ALARA data file, default: ./data")
    parser.add_argument("-s", "--separator", required=False, help=" '_' or '-'")
    parser.add_argument("-t", "--truncation", required=False, help="reset turncation")
    args = vars(parser.parse_args())

    # input
    inp = "alara_inp"
    if args['input'] is not None:
        inp = args['input']

    # number of tasks
    if args['num_tasks'] is not None:
        num_tasks = int(args['num_tasks'])
        print(f"{num_tasks} sub-tasks will be generated")

    # separator
    sep = '_'
    if args['separator'] is not None:
        if args['separator'] not in ['_', '-']:
            raise ValueError(f"separator {args['separator']} not supported!")
        sep = args['separator']

    # alara data
    data = "./data"
    if args['data'] is not None:
        data = args['data']
        print(f"ALARA data: {data}")

    # truncation
    truncation = 1e-12
    if args['truncation'] is not None:
        truncation = float(args['truncation'])
        print(f"use truncation: {truncation}")

    split_alara_inp(inp, num_tasks, sep=sep, truncation=truncation)
    
    # setup sub-task directories
    for i in range(num_tasks):
        os.system(f"mkdir -p task{i}")
        os.system(f"ln -sf {os.path.abspath(data)} task{i}/data")
        # goes into sub-task dir
        print(f"copy/link files for task {i}")
        os.chdir(f"task{i}")
        os.system(f"mv ../{inp}{sep}{i} .")
        os.system(f"ln -sf ../alara_fluxin alara_fluxin")
        os.system(f"ln -sf ../alara_matlib alara_matlib")
        #pbs_generation(i, inp=inp, sep=sep)
        os.chdir("..")
        

if __name__ == '__main__':
    alara_split_task()
