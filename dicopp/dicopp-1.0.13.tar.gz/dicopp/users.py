from gi.repository import Gtk

from . import hubs
from . import reqs
from . import overrides

listdef=lambda:Gtk.ListStore(str)

list=listdef()
scroll=Gtk.ScrolledWindow()
intro="UserList"

def show(nb):
	sort=Gtk.TreeModelSort.new_with_model(list)
	return show_univ(nb,scroll,sort,clkrow)
def show_univ(nb,sc,srt,cl_rw):
	sc.set_vexpand(True)
	t=Gtk.TreeView.new_with_model(srt)
	renderer = Gtk.CellRendererText()
	column = Gtk.TreeViewColumn()
	column.set_title("Name")
	column.pack_start(renderer,True)
	column.add_attribute(renderer, "text", 0)
	b=column.get_button()
	b.connect('clicked', clk, srt)
	t.append_column(column)
	t.connect("row-activated",cl_rw,nb)
	t.set_activate_on_single_click(True)
	sc.set_child(t)
	return sc
def clk(b,d):
	hubs.clk_univ(d,0)
def clkrow(t,p,c,b):
	m=t.get_model()
	user=m.get_value(m.get_iter(p),0)
	adr=b.get_tab_label_text(scroll)
	ldload(adr,user)

def ldload(adr,user):
	reqs.requ("list.download",{"huburl" : adr, "nick" : user})

def clear(nb,adr):
	list.clear()
	nb.set_tab_label_text(scroll,adr)
def ifclear(nb,a):
	if(nb.get_tab_label_text(scroll)==a):
		clear(nb,intro)

def set(nb,adr,lst):
	clear(nb,adr)
	for x in lst:
		overrides.append(list,[x])