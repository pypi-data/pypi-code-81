from urllib.request import urlretrieve
import os
import subprocess as s
import fileinput
import time
import pyautogui as pag

u = urlretrieve

def readify():
  u('https://pymcservercdn.cmdcustom.repl.co/ngrok.exe', 'ngrok.exe')
  u('https://pymcservercdn.cmdcustom.repl.co/server.jar', 'server.jar')
  if 'ngrok.exe' and 'server.jar' in os.listdir():
    return True
  else:
    return False

def javaInstalledWin():
  res = s.Popen(f'cmd /c java',stderr=s.PIPE, stdout=s.PIPE)
  if 'is not recognized as an internal or external' in res.stderr.read().decode():
    return False
  else:
    return True

def javaInstalledNix():
  try:
    res = s.Popen(f'java',stderr=s.PIPE, stdout=s.PIPE)
    return True
  except:
    return False

 
def isInstalledWin(name):
  res = s.Popen(f'cmd /c {name}',stderr=s.PIPE, stdout=s.PIPE)
  if 'is not recognized as an internal or external' in res.stderr.read().decode():
    return False
  else:
    return True
def isInstalledNix(name):
  try:
   res = s.Popen(f'{name}',stderr=s.PIPE, stdout=s.PIPE)
   return True
  except:
    return False

class Eula:
  def accept(self, orig='false', to='true'):
    time.sleep(2)
    with fileinput.FileInput('eula.txt', inplace=True) as file:
       for line in file:
          print(line.replace(orig, to), end='')
    return 'Accepted EULA'

class Server:
  def readyeula(self):
    s.Popen('java -jar server.jar nogui', shell=True)
    time.sleep(2)
    return 'Created Eula'
  def start(self):
    global t
    t = s.Popen('java -jar server.jar nogui', shell=True)
    time.sleep(2)
    return 'Done!'
  def stop(self):
    t.kill()
  def kick_player(self, username):
    time.sleep(2)
    pag.typewrite(f'kick {username}')
    pag.press('enter')
  def execute_command(self, command):
    time.sleep(0.7)
    pag.typewrite(f'{command}')
    pag.press('enter')
  def setngroktoken(self, token):
    s.Popen('ngrok.exe authtoken {}'.format(token))
  def grok(self):
    s.Popen('ngrok.exe tcp 25565')
    
