#!/usr/bin/env python3


import os
import sys
import json
import pprint
import radical.pilot as rp

this_script = os.path.abspath(__file__)
cpn = 8


# ------------------------------------------------------------------------------
#
class Master(rp.raptor.Master):

    @staticmethod
    def descr():
        return rp.TaskDescription({'uid'       : 'raptor.master',
                                   'executable': this_script,
                                   'arguments' : ['master']})

    def __init__(self):
        rp.raptor.Master.__init__(self)

    @staticmethod
    def run():

        master = Master()
        master.submit(descr=Worker.descr(), count=1, cores=cpn, gpus=0)
        master.start()
        master.join()
        master.stop()


# ------------------------------------------------------------------------------
#
class Worker(rp.raptor.Worker):

    @staticmethod
    def descr():
        return rp.TaskDescription({'uid'       : 'raptor.worker',
                                   'executable': this_script,
                                   'arguments' : ['worker']})

    def __init__(self, cfg):
        rp.raptor.Worker.__init__(self, cfg)

    @staticmethod
    def run(cfg):

        worker = Worker(cfg=cfg)
        worker.start()
        worker.join()


# ------------------------------------------------------------------------------
#
class Task(object):

    @staticmethod
    def descr():
        return rp.TaskDescription({
                       'executable'    : 'raptor',
                       'scheduler'     : 'raptor.master',
                       'input_staging' : [{'source': '/etc/passwd',
                                           'target': 'pilot://in.dat',
                                           'action': rp.TRANSFER}],
                       'output_staging': [{'source': 'pilot://out.dat',
                                           'target': 'client://out_client.dat',
                                           'action': rp.TRANSFER}],
                       'arguments'     : [json.dumps({
                           'mode'      : 'exec',
                           'data'      : {'exe' : '/bin/cp',
                                          'args': ['../in.dat', '../out.dat']}
                       })]
                    })


# ------------------------------------------------------------------------------
#
def client():

    def state_cb(task, state):
        print('---> ', task.uid, task.state)

    session = rp.Session()

    try:
        tmgr  = rp.TaskManager(session=session)
        pmgr  = rp.PilotManager(session=session)
        pilot = pmgr.submit_pilots(rp.PilotDescription({
                                   'resource': 'local.localhost',
                                   'runtime' : 10,
                                   'cores'   : 2 * cpn,
                                  }))

        tmgr.add_pilots(pilot)
        tmgr.register_callback(state_cb)

        master = tmgr.submit_tasks(Master.descr())
        task   = tmgr.submit_tasks(Task.descr())

        task.wait(state=['AGENT_STAGING_OUTPUT_PENDING'] + rp.FINAL)

        if task.state == rp.FAILED:
            print('task failed:', task.stderr)
        else:
            pilot.stage_out({'source': 'pilot://out.dat',
                             'target': 'client://out.extra.dat',
                             'action': rp.TRANSFER})

        tmgr.cancel_tasks(uids=master.uid)
        tmgr.wait_tasks()


    finally:
        session.close(download=False)


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    mode = sys.argv[1]
    if mode == 'client':
        client()
    elif mode == 'master':
        Master.run()
    elif mode == 'worker':
        Worker.run(cfg=sys.argv[2])
    else:
        print('undefined mode %s' % mode)
        sys.exit(1)


# ------------------------------------------------------------------------------

