#!/usr/bin/env python
# coding=utf-8

__author__ = "Garrett Bates"
__copyright__ = "© Copyright 2020, Tartan Solutions, Inc"
__credits__ = ["Garrett Bates"]
__license__ = "Apache 2.0"
__version__ = "0.1.5"
__maintainer__ = "Garrett Bates"
__email__ = "garrett.bates@tartansolutions.com"
__status__ = "Development"

"""
   Copyright 2020 Tartan Solutions, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import logging
import asyncio
import signal
import sys
import os
from contextlib import suppress

logging.basicConfig(level=logging.INFO)

async def send_signal(proc_queue, sig):
    proc = await proc_queue.get()
    proc.send_signal(sig)
    proc_queue.put_nowait(proc)

async def run_command(proc_queue):
    """Creates a child process from the args passed in from shell. Restarts until cancelled during shutdown."""
    backoff = 5
    try:
        while True:
            proc = await asyncio.create_subprocess_exec(sys.argv[1], *sys.argv[2:], preexec_fn=os.setpgrp)
            proc_queue.put_nowait(proc)
            returncode = await proc.wait()
            with suppress(asyncio.QueueEmpty):
                # Dequeue the process if its still there.
                proc_queue.get_nowait()
            if returncode and returncode > 0:
                # Process returned error (None = process still running), so initiate backoff mechanism.
                backoff = backoff * 2 if backoff < 300 else 300
                logging.info("")
                logging.info(f" Restarting in {backoff} seconds...")
                logging.info("")
                asyncio.sleep(backoff)
            else:
                backoff = 1
                logging.info("")
                logging.info(" Restarting...")
                logging.info("")

    except asyncio.CancelledError:
        proc.terminate()
        await proc.wait() # Must wait for termination to finish to avoid zombies.
            

async def shutdown():
    """Cancel all running tasks in anticipation of exiting."""
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]  # pylint: disable=expression-not-assigned

    logging.info('Canceling outstanding tasks')
    await asyncio.gather(*tasks)


def main():
    """Entrypoint for the entrypoint."""
    loop = asyncio.get_event_loop()
    proc_queue = asyncio.Queue(maxsize=1)

    # Forward these signals to child process.
    loop.add_signal_handler(signal.SIGHUP, lambda: asyncio.create_task(send_signal(proc_queue, signal.SIGTERM)))
    loop.add_signal_handler(signal.SIGUSR1, lambda: asyncio.create_task(send_signal(proc_queue, signal.SIGUSR1)))

    # SIGTERM and SIGINT should cancel all tasks and exit.
    for s in {signal.SIGTERM, signal.SIGINT}:  # pylint: disable=no-member
        # logging.info(f'adding handlers for {s.name}')
        loop.add_signal_handler(s, lambda: asyncio.create_task(shutdown()))

    # run_command will continually restart the child proc until it is cancelled.
    loop.run_until_complete(run_command(proc_queue))
