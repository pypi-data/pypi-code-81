from gi.repository import Gtk

from . import reqs
from . import users
from . import flist
from . import overrides

list=users.listdef()
page=Gtk.ScrolledWindow()

def show(nb):
	page.set_vexpand(True)
	sort=Gtk.TreeModelSort.new_with_model(list)
	return users.show_univ(nb,page,sort,clkrow)

def clkrow(t,p,c,b):
	m=t.get_model()
	user=m.get_value(m.get_iter(p),0)
	flist.set(b,user)

def set():
	s=";"
	r=reqs.reque("list.local",{"separator" : s})
	list.clear()
	usrs=r.split(s)
	for x in usrs:
		overrides.append(list,[x])