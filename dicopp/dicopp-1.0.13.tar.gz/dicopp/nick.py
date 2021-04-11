from gi.repository import Gtk

import random
import xml.etree.ElementTree as ET

from . import stor2
from . import daem
from . import share

def rand4(a):
	s=str(a)
	while len(s)<4:
		s='0'+s
	return s
name=Gtk.EntryBuffer(text='dico_'+rand4(random.randint(0,9999)))

def confs():
	return name
def store(d):
	d['nick_name']=name.get_text()
def restore(d):
	name.set_text(d['nick_name'],-1)
def ini(restart):
	f=stor2.get_file()
	t = ET.parse(f)
	root = t.getroot()
	se = root.find(stor2.set)
	b=see(se,'Nick','string',name)
	c=share.ini(root) or b
	#Slots not working r|=see(se,'Slots','int',slots)
	if c:
		if restart:
			daem.dclose()
		t.write(f)
		if restart:
			daem.restart()
	return c

def see(se,n,t,b):
	txt=b.get_text()
	s = se.find(n)
	if s==None:
		s=ET.SubElement(se,n)
		s.set('type',t)
		s.text=txt
		return True
	elif txt!=s.text:
		s.text=txt
		return True
	return False
