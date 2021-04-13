# -*- coding: utf-8 -*-
import click
import os
import shutil
import uuid

dirname = os.path.dirname
basename = os.path.basename

def split(path):
  return os.path.normpath(path).split(os.path.sep)

join = os.path.join

def random_name():
  return uuid.uuid4().hex

def is_single_child(path):
  base, _ = os.path.split(path)
  if base in ('', '.'): return False
  return len(os.listdir(base)) == 1

def replace(path, newname, level=0):
  segments = split(path)
  level = len(segments)-level
  segments[level-1] = newname
  return join(*segments)

def renamedir(path, newname, level=0):
  segments = split(path)
  level = len(segments)-level
  oldpath = join(*segments[:level])
  newpath = replace(oldpath, newname)
  # print 'rename %s\n       %s' % (oldpath, newpath)
  os.rename(oldpath, newpath)
  return newpath

def moveall(src, dest):
  #print 'move %s\n     %s' % (src, dest)
  files = os.listdir(src)
  for f in files:
    shutil.move(join(src, f), dest)

def rmdir(path):
  #print 'rmdir %s' % path
  os.rmdir(path)

def moveup(src, separator):
  segments = split(src)
  name = separator.join([segments[-2], segments[-1]])
  rnd = renamedir(src, random_name())
  renamedir(src, name, level=1)
  rnd = replace(rnd, name, level=1)
  moveall(rnd, dirname(rnd))
  rmdir(rnd)

def walkdirs(path = '.'):
  out = []
  for root, dirs, files in os.walk(".", topdown=False):
    for name in dirs:
      dirpath = join(root, name)
      out.append(dirpath)
  return out

def dir_to_flatten():
  try:
    return next(d for d in walkdirs() if is_single_child(d))
  except:
    return None

@click.command(help='Move single dirs one level up, combine names')
@click.option('--sep', default=' - ', help='separator for joining directory names')
def flatten(sep):
  while dir_to_flatten():
    d = dir_to_flatten()
    if click.confirm(d):
      moveup(d, sep)

if __name__ == '__main__':
    flatten()