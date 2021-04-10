""" 
	This is a extention of tkinter
	Any error is welcome to be pointed out 
	via 'charles.shht@gmail.com'.
"""
__version__ = '0.0.1'

import tkinter as tk

TKGFLAG = False

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

	def test_pack(self):
		self.bar_frame.configure(background="gold",width=400,height=30)
		self.files_frame.configure(background="red",width=70,height=200)
		self.details_frame.configure(background="green",width=260,height=200)
		self.attributes_frame.configure(background="blue",width=70,height=200)
		self.logs_frame.configure(background="black",width=400,height=40)
		self.pack()

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
