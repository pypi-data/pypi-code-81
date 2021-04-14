
from gi.repository import Gtk

import xml.etree.ElementTree as ET
import appdirs
import os.path

from . import limit
from . import nick
from . import sets

file=Gtk.EntryBuffer()
set='Settings'

def get_file_default():
	return os.path.join(appdirs.user_config_dir('eiskaltdc++'),'DCPlusPlus.xml')
def get_file():
	a=file.get_text()
	if a:
		return os.path.expandvars(a)
	return get_file_default()

def ini():
	f = get_file()
	t = ET.parse(f)
	root = t.getroot()
	s = root.find(set)
	limit.start=int(s.find('TotalUpload').text)
def confs():
	f=Gtk.Frame(label="External data file settings")
	g=Gtk.Grid()
	lb=Gtk.Label(halign=Gtk.Align.START,label="Location (blank for default)")
	g.attach(lb,0,0,1,1)
	g.attach(confs_loc(),1,0,1,1)
	lb=Gtk.Label(halign=Gtk.Align.START,label="Nick name")
	g.attach(lb,0,1,1,1)
	en=sets.entries(nick.confs())
	g.attach(en,1,1,1,1)
	f.set_child(g)
	return f
def store(d):
	d['ext_file']=file.get_text()
def restore(d):
	file.set_text(d['ext_file'],-1)

def confs_loc():
	en=sets.entries(file)
	if file.get_text():
		return en
	bx=Gtk.Box()
	bx.append(en)
	bx.append(Gtk.Label(label=get_file_default()))
	return bx