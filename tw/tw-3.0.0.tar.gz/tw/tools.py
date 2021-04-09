# Copyright 2020 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
r"""TensorWrapper Tools
"""
import os
import re
import argparse
import sys
import glob
import shutil
import pickle
import psutil
import subprocess
import psutil
import xml.etree.ElementTree as ET
import time

import tw
from tw import logger

from tensorboard.backend.event_processing import event_accumulator

import matplotlib.pyplot as plt
import matplotlib.pylab as plb

#!<----------------------------------------------------------------------------
#!< monitor
#!<----------------------------------------------------------------------------


def monitor_kill(process_name):
  for proc in psutil.process_iter():
    try:
      pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cmdline'])
    except psutil.NoSuchProcess:
      pass
    else:
      for cmd in pinfo['cmdline']:
        if process_name in cmd and 'tw.tools' not in cmd:
          print(pinfo)
          os.system('kill -9 %d' % pinfo['pid'])
          break


def monitor_usage(proc_name):
  r"""monitor cpu and gpu activity status.

    e.g.
      python -m tw.tools monitor --task usage --src name

  """
  logger.init('monitor.{}.{}.log'.format(proc_name, int(time.time())), './')
  pid = None
  for proc in psutil.process_iter():
    pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cmdline'])
    for cmd in pinfo['cmdline']:
      if proc_name in cmd:
        if pinfo['pid'] == os.getpid():
          continue
        pid = pinfo['pid']
        break
    if pid:
      break

  proc = psutil.Process(pid=pid)
  logger.info('=> {}'.format(proc))

  while True:
    memory_rss = proc.memory_info().rss / 1024.0 / 1024.0
    memory_vms = proc.memory_info().vms / 1024.0 / 1024.0
    memory_shared = proc.memory_info().shared / 1024.0 / 1024.0
    memory_text = proc.memory_info().text / 1024.0 / 1024.0
    cpu_usage = proc.cpu_percent(interval=1)
    num_thread = proc.num_threads()
    tick = int(time.time() * 10**3)  # precision to ms
    logger.info('{}, cpu, {}, {}, {}, {}, {}, {}, {}'.format(
        tick, num_thread, memory_rss, memory_vms,
        memory_shared, memory_text, cpu_usage, num_thread))
    try:
      res = subprocess.check_output('nvidia-smi -q -x', shell=True)
      s = 'gpu'
      if res is not None:
        res = ET.fromstring(res)
        for g in res.findall('gpu'):
          s += ', ' + g.find('fb_memory_usage').find('used').text.split(' MiB')[0]  # nopep8
      tick = int(time.time() * 10**3)  # precision to ms
      logger.info('{}, {}'.format(tick, s))
    except:
      pass


def monitor_consist(process_name):
  proc_name = process_name
  while(1):
    for proc in psutil.process_iter():
      try:
        pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cmdline'])
      except psutil.NoSuchProcess:
        pass
      else:
        for cmd in pinfo['cmdline']:
          if proc_name in cmd:
            if pinfo['pid'] == os.getpid():
              continue
            print(cmd)
            print(pinfo)
            try:
              monitor_usage(pinfo['pid'])
            except:
              break
    time.sleep(5)

#!<----------------------------------------------------------------------------
#!< media
#!<----------------------------------------------------------------------------

#!<----------------------------------------------------------------------------
#!< tensor event
#!<----------------------------------------------------------------------------

#!<----------------------------------------------------------------------------
#!< checkpoint
#!<----------------------------------------------------------------------------


if __name__ == "__main__":
  # domain first
  domain = sys.argv[1]
  assert domain in ['monitor', 'media', 'event', 'checkpoint', ]

  # parser
  parser = argparse.ArgumentParser()

  if domain == 'monitor':
    parser.add_argument('--task', type=str, choices=['usage', 'plot', 'kill'])
    parser.add_argument('--src', type=str, default='pid name or process name.')
    parser.add_argument('--dst', type=str, default='output folder for plot.')
    parser.add_argument('--legend', type=str, default=None)
    args, _ = parser.parse_known_args()

    # if args.task == 'kill':
    #   monitor_kill(args.src)

    # elif args.task == 'usage':
    #   monitor_usage()

    # elif args.task == 'plot':
    #   monitor_plot()

  elif domain == 'media':
    parser.add_argument('--task', type=str, choices=['vid2img', 'img2vid', 'concat_image'])
    parser.add_argument('--src', type=str, default='image folder, video path, image paths.')
    parser.add_argument('--dst', type=str, default='output folder.')
    args, _ = parser.parse_known_args()

  elif domain == 'event':
    parser.add_argument('--task', type=str, choices=['plot', 'count', 'dump', 'compare'])
    parser.add_argument('--src', type=str, default='')
    parser.add_argument('--dst', type=str, default='')
    args, _ = parser.parse_known_args()

  elif domain == 'checkpoint':
    parser.add_argument('--task', type=str, choices=['replace_prefix'])
    parser.add_argument('--src', type=str, default='')
    parser.add_argument('--dst', type=str, default='')
    args, _ = parser.parse_known_args()

  else:
    raise NotImplementedError(domain)
