from os import*
from time import*
def pip(pakage):
    system("pip install " + pakage)
def shutdown(time = 60):
    system("shutdown -s -t " + str(time))
def noshutdown():
    system("shutdown -a")
def color(cor):
    system("color " + str(cor))
def cd(where):
    system("cd " + where)
