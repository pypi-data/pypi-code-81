
from gi.repository import Gtk

import xml.etree.ElementTree as ET
import urllib.request
import os.path

listdef=lambda:Gtk.ListStore(str,int,str)

from . import base
from . import hubscon
from . import sets
from . import overrides
from . import main

addr=Gtk.EntryBuffer(text='https://www.te-home.net/?do=hublist&get=hublist.xml')
file=Gtk.EntryBuffer(text='hublist.xml')
lim=Gtk.EntryBuffer(text='200')

list=listdef()
sort=Gtk.TreeModelSort.new_with_model(list)

from enum import IntEnum
class COLUMNS(IntEnum):
	ADDRESS=0
	USERS=1
	COUNTRY=2
def treedef(lst,act,clkrow,data):
	tree=Gtk.TreeView.new_with_model(lst)
	col(tree,'Address',COLUMNS.ADDRESS,act)
	col(tree,'Users',COLUMNS.USERS,act)
	col(tree,'Country',COLUMNS.COUNTRY,act)
	tree.connect("row-activated",clkrow,data)
	tree.set_activate_on_single_click(True)
	return tree
def col(tr,tx,ix,act):
	renderer = Gtk.CellRendererText()
	column = Gtk.TreeViewColumn()
	column.set_title(tx)
	column.set_resizable(True)
	column.pack_start(renderer,True)
	column.add_attribute(renderer, "text", ix)
	b=column.get_button()
	b.connect('clicked', act, ix)
	tr.append_column(column)

def confs():
	f=Gtk.Frame(label="Hub List")
	g=Gtk.Grid()
	lb=Gtk.Label(halign=Gtk.Align.START,label="File address")
	g.attach(lb,0,0,1,1)
	en=sets.entries(addr)
	g.attach(en,1,0,1,1)
	lb=Gtk.Label(halign=Gtk.Align.START,label="File fallback location")
	g.attach(lb,0,1,1,1)
	en=sets.entries(file)
	g.attach(en,1,1,1,1)
	lb=Gtk.Label(halign=Gtk.Align.START,label="Maximum number of entries")
	g.attach(lb,0,2,1,1)
	en=sets.entries(lim)
	g.attach(en,1,2,1,1)
	f.set_child(g)
	return f
def store(d):
	d['hub_file']=addr.get_text()
	d['hub_file_fallback']=file.get_text()
	d['hub_limit']=lim.get_text()
def restore(d):
	addr.set_text(d['hub_file'],-1)
	file.set_text(d['hub_file_fallback'],-1)
	lim.set_text(d['hub_limit'],-1)

def reset():
	list.clear()
	ini()

def clk_univ(lst,ix):
	n=lst.get_sort_column_id()
	if n[1]!=Gtk.SortType.ASCENDING:
		lst.set_sort_column_id(ix,Gtk.SortType.ASCENDING)
	else:
		lst.set_sort_column_id(ix,Gtk.SortType.DESCENDING)
def clk(b,ix):
	clk_univ(sort,ix)
def show():
	wn=Gtk.ScrolledWindow()
	wn.set_vexpand(True)
	tree=treedef(sort,clk,hubscon.add,sort)
	wn.set_child(tree)
	return wn

def ini():
	try:
		tree = ET.ElementTree(file=urllib.request.urlopen(addr.get_text()))
	except Exception:
		t=os.path.expandvars(file.get_text())
		d=os.path.dirname(t)
		if d=="":
			tree = ET.parse(main.get_root_file(t))
		else:
			tree = ET.parse(t)
	root = tree.getroot()
	try:
		hbs=root.find("Hubs").findall("Hub")
	except Exception:
		return
	mx=min(int(lim.get_text()),len(hbs))
	for i in range(mx):
		attrs=hbs[i].attrib
		if ('Secure' in attrs) and (attrs['Secure']):
			huburl=attrs['Secure']
		elif 'Address' in attrs:
			huburl=attrs['Address']
		else:
			continue
		if ('Users' in attrs) and ('Country' in attrs):
			overrides.append(list,[huburl,int(attrs['Users']),attrs['Country']])
