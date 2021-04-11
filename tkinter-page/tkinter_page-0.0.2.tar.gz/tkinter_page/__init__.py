""" 
	This is a extention of tkinter
	Any error is welcome to be pointed out 
	via 'charles.shht@gmail.com'.
"""
__version__ = '0.0.2'

import tkinter as tk
import tkinter.ttk as ttk


"""
#This is a example to build an DesktopFrame. 

import tkinter as tk
import tkinter_page as tkp

window = tk.Tk()

# Way1: Generate child frame before DesktopFrame by building a dict
bar_frame = {"background":"gold","width":400,"height":30}
files_frame = {"background":"red","width":70,"height":200}

# Generate a DesktopFrame
bframe = tkp.DesktopFrame(window,log=True,bar_frame=bar_frame,files_frame=files_frame)

# Way2: Generate child frame after DesktopFrame by building a dict
details_frame = {"background":"green","width":260,"height":200}
bframe.set_details_frame(details_frame)
bframe.set_attributes_frame({"background":"blue","width":70,"height":200})

# Way3: Generate child frame after DesktopFrame by building a frame
# If youo use the third way, be careful that you should define the master.
# --------------------------------------------------------------
# |  master     |    child frame                               |
# | base_frame  | bar_frame, logs_frame                        |
# | mid_frame   | files_frame, details_frame, attributes_frame |
# --------------------------------------------------------------
logs_frame = tk.Frame(bframe.base_frame,background="black",width=400,height=40)
bframe.set_logs_frame(logs_frame)

# Pack and Run
bframe.pack()
window.mainloop()
"""


class DesktopFrame():
	"""Traditional Desktop Application Layout"""
	def __init__(self, master=None, cnf={}, **kw):
		""" Normally software application follows a master-to-detail navigation style.
		—————————————————————————————————————————————————————————————
		|                  Quick Access Bar  (bar_frame)             |
		—————————————————————————————————————————————————————————————
		|         |                                   |              |
		|         |                                   |              |
		|         |                                   |   Attribute  |
		|         |                                   |      and     |
		| Project |                                   | Configuration|
		|  Files  |             Details Pane          |     Pane     |      
		|Navigator|                                   |              |
		|         |           (details_frame)         |              |
		|         |                                   | (attributes_frame)
		|(files_frame)                                |              |
		|         |                                   |              |
		|         |                                   |              |
		—————————————————————————————————————————————————————————————
		|                    Console and Logs Pane                   |
		|                           (logs_frame)                     |
		——————————————————————————————————————————————————————————————


		Old resource names: background, bd, bg, borderwidth, class,
		colormap, container, cursor, height, highlightbackground,
		highlightcolor, highlightthickness, relief, takefocus, visual, width."""

		# Get Setting and Child Frame Configure 
		if "log" in kw:
			self.log = kw["log"]
			del kw["log"]
		else:
			self.log = False

		if self.log:
			print("\nGetting Child Frame:")
		for child_frame in ["bar_frame","files_frame",\
			"details_frame","attributes_frame","logs_frame"]:
			exec('self.{}_dict = {{}}'.format(child_frame))
			if child_frame in kw:
				exec('self.{}_dict = eval(\'kw["{}"]\')'.format(child_frame,child_frame))
				if self.log:
					print(child_frame,eval('self.{}_dict'.format(child_frame)))
				exec('del kw["{}"]'.format(child_frame))
			else:
				exec('self.{} = None'.format(child_frame))
				if self.log:
					print(child_frame,eval('self.{}'.format(child_frame)))

		# Base Frame Init
		if self.log:
			print("\nBase Frame Init")
		cnf = tk._cnfmerge((cnf, kw))	
		extra = ()
		if 'class_' in cnf:
		    extra = ('-class', cnf['class_'])
		    del cnf['class_']
		elif 'class' in cnf:
		    extra = ('-class', cnf['class'])
		    del cnf['class']
		if self.log:
			print("Creat base_frame and mid_frame")
		self.base_frame = tk.Frame(master, cnf)
		self.mid_frame = tk.Frame(master=self.base_frame)

		# Generate Child Frames
		if self.log:
			print("\nGenerate Child Frames")
		if self.log: print("Generate bar_frame")
		self.bar_frame = tk.Frame(self.base_frame,self.bar_frame_dict)
		if self.log: print("Generate files_frame")
		self.files_frame = tk.Frame(self.mid_frame,self.files_frame_dict)
		if self.log: print("Generate details_frame")
		self.details_frame = tk.Frame(self.mid_frame,self.details_frame_dict)
		if self.log: print("Generate attributes_frame")
		self.attributes_frame = tk.Frame(self.mid_frame,self.attributes_frame_dict)
		if self.log: print("Generate logs_frame")
		self.logs_frame = tk.Frame(self.base_frame,self.logs_frame_dict)

	def set_bar_frame(self,frame):
		if self.log: print("\nReset bar_frame")
		if type(frame) == dict:
			self.bar_frame_dict= frame
			self.bar_frame = tk.Frame(self.base_frame,self.bar_frame_dict)
		elif type(frame) == tk.Frame:
			self.bar_frame = frame

	def set_files_frame(self,frame):
		if self.log: print("\nReset files_frame")
		if type(frame) == dict:
			self.files_frame_dict = frame
			self.files_frame = tk.Frame(self.mid_frame,self.files_frame_dict)
		elif type(frame) == tk.Frame:
			self.files_frame = frame

	def set_details_frame(self,frame):
		if self.log: print("\nReset details_frame")
		if type(frame) == dict:
			self.details_frame_dict = frame
			self.details_frame = tk.Frame(self.mid_frame,self.details_frame_dict)
		elif type(frame) == tk.Frame:
			self.details_frame = frame

	def set_attributes_frame(self,frame):
		if self.log: print("\nReset attributes_frame")
		if type(frame) == dict:
			self.attributes_frame_dict = frame
			self.attributes_frame = tk.Frame(self.mid_frame,self.attributes_frame_dict)
		elif type(frame) == tk.Frame:
			self.attributes_frame = frame

	def set_logs_frame(self,frame):
		if self.log: print("\nReset logs_frame")
		if type(frame) == dict:
			self.logs_frame_dict = frame
			self.logs_frame = tk.Frame(self.base_frame,self.logs_frame_dict)
		elif type(frame) == tk.Frame:
			self.logs_frame = frame

	def pack(self):
		self.base_frame.pack(fill='both',expand=1)
		self.bar_frame.pack(side='top',fill='x')
		self.mid_frame.pack(side='top',fill='x')
		self.files_frame.pack(side='left',fill='y',expand=1)
		self.details_frame.pack(side='left',fill='both',expand=1)
		self.attributes_frame.pack(side='right',fill='y',expand=1)
		self.logs_frame.pack(side='bottom',fill='x')

	def pack_forget(self):
		for child_frame in ["bar_frame","files_frame",\
			"details_frame","attributes_frame","logs_frame"]:
				exec('self.{}.pack_forget()'.format(child_frame)) 

	def destory():
		for child_frame in ["bar_frame","files_frame",\
			"details_frame","attributes_frame","logs_frame"]:
				exec('self.{}.destory()'.format(child_frame)) 


class SplitViewFrame():
	""" Thisinheritsthe master-to-detail interface from desktop UI, 
	where changes in the primary view (the master) drive changes in a 
	secondary view (the detail).
	"""

	def __init__(self, master=None, cnf={}, **kw):
		""" Normally software application follows a master-to-detail navigation style.
		——————————————————————————————————————————————————————————————
		|Back Content Edit|                                          |
		|—————————————————|                                          |
		|                 |                                          |
		|      Item1      |                                          |
		|—————————————————|                                          |
		|                 |                                          |
		|      Item2      |               Details Pane               |
		|—————————————————|                                          |
		|                 |              (details_frame)             |
		|      Item3      |                                          |
		|—————————————————|                                          |
		|                 |                                          |
		|      Item4      |                                          |
		|—————————————————|                                          |
		|                 |                                          |
		|      Itemn      |                                          |
		——————————————————————————————————————————————————————————————

		Old resource names: background, bd, bg, borderwidth, class,
		colormap, container, cursor, height, highlightbackground,
		highlightcolor, highlightthickness, relief, takefocus, visual, width."""
		pass


class ComponentsList(list):
	"""
	"""
	def __init__(self, master=None, cnf={}, **kw):
		pass

	def pack():
		pass

	def pack_forget():
		pass

	def destory():
		pass


"""
#This is a example to build an Page. 

import tkinter as tk
import tkinter_page as tkp

window = tk.Tk()

base_frame = tk.Frame(window,width=1000,height=600)

# First we creat three child pages
# We can creat a pack way for a page
def pack_way1():
	print("child_page1")
	label1.pack(fill='x')
child1 = tkp.Page(base_frame,"child1",pack_way=pack_way1)
label1 = tk.Label(base_frame,text="child1",width=10,height=2)
child1.add_component(label1)

def pack_way2():
	print("child_page2")
	label2.pack()
child2 = tkp.Page(base_frame,"child2",pack_way=pack_way2)
label2 = tk.Label(base_frame,text="child2",width=10,height=2)
child2.add_component(label2)

# We can also use auto pack way(do not need a pack way func)
child3 = tkp.Page(base_frame,"child3")
label3 = tk.Label(base_frame,text="child3",width=10,height=2)
child3.add_component(label3)

# make child page list
child_page = [child1,child2,child3]

# construct father page
page1 = tkp.Page(base_frame,"page1",show_child=True,\
	flip="Combobox",child_page=child_page,current=0)

# Pack Father Page
# you can also use
# page1.pack(show_child=True)
# to auto show the current child page
base_frame.pack(fill='both',expand=1)
page1.pack()

window.mainloop()
"""


class Page():
	""" 
	id_: (str) An ID of a page.
	master: (object) master of a page.
	flip: (str or None) page flip way.
	flip_combobox: (object) If flip=="combobox",
		use combobox to change child page.
	child_page: (list) child page.
	child_page_id: (list) child page id.
	current: (int) the number of child page
		that show now.
	show_child: (bool) wherther auto show child page
	pack_way: (function) whether to pack a page
	page_member: (list) compononts in a page
	"""
	def _update_child_page_id(self):
		self.child_page_id = []
		for item in self.child_page:
			self.child_page_id.append(item.id_)

	def __init__(self, master, id_, cnf={}, **kw):
		""" 
		"""
		# Get Page ID and master
		if type(id_) != str:
			return False
		self.id_ = id_
		self.master = master

		# get page components
		self.page_member = []

		# Get Child Pages 
		self.child_page = []
		if "child_page" in kw:
			if type(kw["child_page"]) == list:
				self.child_page = kw["child_page"]
		self._update_child_page_id()

		# Set current child page
		if ("current" not in kw) or (kw["current"] == None):
			# Do not have child page
			self.current = -1
		else:
			self.current = kw["current"]

		# wheather auto show child page
		if ("show_child" not in kw) or (kw["show_child"] == False)\
			or (type(kw["show_child"]) != bool):
			# Do not have child page
			self.show_child = False
		else:
			self.show_child = kw["show_child"]

		# Genrate Page Flipping type
		if ("flip" not in kw) or (kw["flip"] == None):
			# Do not have child page
			self.flip = None
		elif kw["flip"] == 'Combobox':
			# Use Combobox to flip child pages
			self.flip = 'Combobox'
			self.flip_combobox = ttk.Combobox(self.master)
			self.flip_combobox['values'] = self.child_page_id
			self.flip_combobox.bind("<<ComboboxSelected>>",\
				self.set_current)
		elif kw["flip"] == 'Tree':
			# Use Button or other components to flip child pages
			pass

		# whether to pack a page
		if ("pack_way" not in kw) or (kw["pack_way"] == None):
			# Do not have child page
			self.pack_way = None
		else:
			self.pack_way = kw["pack_way"]

	def __str__(self):
		return "Page: "+str(self.id_)

	def set_current(self,event=None,new_page=None):
		""" change child page """
		# Get new page number
		if self.flip == 'Combobox':
			if new_page == None:
				new_page = self.flip_combobox.current()
			elif type(new_page) == int:
				pass
			else:
				return False
		elif self.flip == 'Tree':
			pass

		# Check if need flip page
		if self.current == new_page:
			return False

		# Flip page
		if self.current != -1:
			self.child_page[self.current].pack_forget()
		self.pack_current(new_page)

	def pack_current(self,new_page):
		if type(new_page)!=int:
			return False
		self.child_page[new_page].pack()
		self.current = new_page

	def pack(self,auto=True,show_child=False):
		# pack components and flip component
		if self.pack_way != None:
			self.pack_way()
		else:
			for item in self.page_member:
				item.pack()
			if auto == True:
				self.pack_combobox()

		# pack child page
		if (show_child or self.show_child) and self.current!=-1:
			self.child_page[self.current].pack()

	def add_component(self,item):
		self.page_member.append(item)

	def set_pack_way(self,pack_way):
		""" pack_way is a function that define the way
		a page packed"""
		self.pack_way = pack_way

	def pack_combobox(self):
		if self.flip == "Combobox":
			self.flip_combobox.pack()

	def pack_forget(self):
		for item in self.child_page:
			item.pack_forget()
		for item in self.page_member:
			item.pack_forget()

	def destory(self):
		for item in self.child_page:
			item.destory()
		for item in self.page_member:
			item.destory()
		self.child_page.clear()
		self.page_member.clear()
