#!/usr/bin/env python3

__author__    = 'RADICAL-Cybertools Team'
__email__     = 'info@radical-cybertools.org'
__copyright__ = 'Copyright 2020-2021, The RADICAL-Cybertools Team'
__license__   = 'MIT'

from random import randint

import radical.pilot as rp

from radical.pilot.states import _task_state_progress

RESOURCE_LABEL      = 'local.localhost'
SMT_LEVEL           = 4
N_CORES_PER_NODE    = 42 * SMT_LEVEL
N_GPUS_PER_NODE     = 6

N_EXEC_NODES        = 1000
N_SUB_AGENTS        = 1

TASK_DURATION_RANGE = [20,30]
N_GENERATIONS       = 5

RUN_TIME            = 1000


# ------------------------------------------------------------------------------
#
def generate_task_cores(num_nodes, cores_per_node):
    # generate cores per task (1..cores_per_node) to fit all available cores
    cores_list, cores, cores_avail = [], 1, num_nodes * cores_per_node
    while True:
        if cores_avail - cores >= 0:
            cores_list.append(cores)
            cores_avail -= cores
            if not cores_avail:
                break
            if cores == cores_per_node:
                cores = 1
            else:
                cores += 1
            continue
        cores -= 1  # equal to (cores_per_node - last_generated_cores)
    cores_list.sort(reverse=True)
    # fit generated cores into available nodes
    # (re-order, thus summary of consequent cores will be equal cores_per_node)
    output = []
    cores_per_node_avail, idx, tag_list, tag_id = cores_per_node, 0, [], 0
    while True:
        if cores_per_node_avail - cores_list[idx] >= 0:
            tag_list.append((cores_list.pop(idx), tag_id))
            cores_per_node_avail -= tag_list[-1][0]
            if not cores_per_node_avail:
                size = len(tag_list)
                # output will contain tuples: <n_cores, node_id, n_node_tasks>
                output.extend(zip(*(list(zip(*tag_list)) + [(size,) * size])))
                if not cores_list:
                    break
                cores_per_node_avail, idx = cores_per_node, 0
                del tag_list[:]
                tag_id += 1
            continue
        idx += 1
    return output


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':
    session = rp.Session()
    try:
        pmgr = rp.PilotManager(session=session)
        tmgr = rp.TaskManager(session=session)
        tmgr.add_pilots(pmgr.submit_pilots(
            rp.PilotDescription({
                'resource'     : RESOURCE_LABEL,
                'nodes'        : (N_EXEC_NODES + N_SUB_AGENTS),
              # 'gpus'         : (N_EXEC_NODES + N_SUB_AGENTS) * N_GPUS_PER_NODE,
                'runtime'      : RUN_TIME,
              # 'input_staging': ['hello_rp.sh']
                 })))
        task_cores_list = generate_task_cores(N_EXEC_NODES, N_CORES_PER_NODE)

        for generation_id in range(N_GENERATIONS):

            tds = list()
            saved_node_id = -1

            for task_cores, node_id, _ in task_cores_list:

              # tag_id = '%s%s' % (generation_id, node_id)
                # set GPUs to the first task on a shared (tagged) node
                gpu_processes = 0

                if node_id != saved_node_id:
                    gpu_processes = N_GPUS_PER_NODE
                    saved_node_id = node_id

                tds.append(rp.TaskDescription({
                           # 'tags'          : {'colocate': tag_id},
                             'cpu_processes' : task_cores,
                             'cpu_threads'   : 1,
                             'gpu_processes' : gpu_processes,
                             'executable'    : '/bin/sleep',
                             'arguments'     : [randint(*TASK_DURATION_RANGE)],
                           # 'input_staging' : [
                           #     {'source'   : 'pilot: ///hello_rp.sh',
                           #      'target'   : 'task : ///hello_rp.sh',
                           #      'action'   : rp.LINK}]
                       }))
            tmgr.submit_tasks(tds)
        tmgr.wait_tasks()
    finally:
        session.close(download=True)


# ------------------------------------------------------------------------------

