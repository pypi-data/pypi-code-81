import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,GLib
import os.path

from . import base
from . import layout 
from . import limit
from . import log
from . import stor2
from . import nick
from . import hubs
from . import hubscon
from . import daem
from . import search
from . import dload
from . import com

def get_root_file(f):
	return os.path.join(os.path.dirname(os.path.realpath(__file__)),f)

def quit(widget, mainloop):
	base.write(widget)
	daem.close(False)#in base.write is log, can require daemon open
	limit.close()
	hubscon.close()
	search.close()
	dload.close()
	com.close()
	mainloop.quit()
	return True

def main():
	mainloop = GLib.MainLoop()
	win = Gtk.Window()
	win.set_title('Direct Connect')
	d=base.read(win)
	layout.show(win)
	limit.open(win)
	log.ini()
	stor2.ini()
	nick.ini(False)
	hubs.ini()
	win.connect('close-request', quit, mainloop)
	daem.dopen()
	base.read2(d)#after daemon start
	win.show()
	mainloop.run()

if __name__ == "__main__":
    main()
