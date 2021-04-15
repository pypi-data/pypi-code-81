""" 
	This is a extention of tkinter
	Any error is welcome to be pointed out 
	via 'charles.shht@gmail.com'.
"""
__version__ = '0.0.3'

import tkinter as tk
import tkinter.ttk as ttk

__all__ = ["DesktopFrame", "Page"]

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
	"""
	Traditional Desktop Application Layout

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
	
	Attributes:
		log (bool): Whether to print the detail of running
		bar_frame (tk.Frame): Quick Access Bar
		files_frame (tk.Frame): Project Files Navigator
		details_frame (tk.Frame): Details Pane
		attributes_frame (tk.Frame): Attribute and Configuration Pane
		logs_frame (tk.Frame): Console and Logs Pane
	"""

	log = False

	def __init__(self, master=None, cnf={}, **kw):
		""" Normally software application follows a master-to-detail navigation style.
		"""

		# Get Setting
		if "log" in kw:
			self.set_log(kw['log'])

		# Base Frame Init
		if self.log:
			print("Creat base_frame and mid_frame")
		self.base_frame = tk.Frame(master)
		self.mid_frame = tk.Frame(master=self.base_frame)

		# Child Frame Configure 
		if self.log:
			print("\nGetting Child Frame:")
		for child_frame in ["bar_frame","files_frame",\
			"details_frame","attributes_frame","logs_frame"]:
			if child_frame in kw:
				exec('self.set_{}(eval(\'kw["{}"]\'))'.format(child_frame,child_frame))
			else:
				exec('self.set_{}(None)'.format(child_frame))

	def set_log(self,log=False):
		""" Set Parameter Log 
		Args:
			log (bool or int or None, optional): Whether 
				to console out the running logs 
		"""
		if log:
			self.log = True
		else:
			self.log = False

	def set_bar_frame(self,frame=None):
		""" Set Bar Frame 

		Args:
			frame (None or tk.Frame or dict, optional):
				Set bar_frame, if None, set bar frame null,
				if dict, set bar frame accroding to dict,
				if tk.Frame, assign frame to bar frame.

		Raises:
			ValueError: wrong type of frame.
		"""
		if self.log: print("\nSet bar_frame")
		if frame == None:
			# Generate a empty frame
			self.bar_frame = tk.Frame(self.base_frame)
		elif type(frame) == dict:
			# Generate frame accroding to a dict
			self.bar_frame = tk.Frame(self.base_frame,frame)
		elif type(frame) == tk.Frame:
			# Directly assign a frame
			self.bar_frame = frame
		else:
			raise ValueError("You should input None or dict or class Frame.")

	def set_files_frame(self,frame=None):
		""" Set Files Frame 

		Args:
			frame (None or tk.Frame or dict, optional):
				Set bar_frame, if None, set Files frame null,
				if dict, set Files frame accroding to dict,
				if tk.Frame, assign frame to Files frame.

		Raises:
			ValueError: wrong type of frame.
		"""
		if self.log: print("\nSet files_frame")
		if frame == None:
			# Generate a empty frame
			self.files_frame = tk.Frame(self.mid_frame)
		elif type(frame) == dict:
			# Generate frame accroding to a dict
			self.files_frame = tk.Frame(self.mid_frame,frame)
		elif type(frame) == tk.Frame:
			# Directly assign a frame
			self.files_frame = frame
		else:
			raise ValueError("You should input None or dict or class Frame.")

	def set_details_frame(self,frame=None):
		""" Set Details Frame 

		Args:
			frame (None or tk.Frame or dict, optional):
				Set bar_frame, if None, set Details frame null,
				if dict, set Details frame accroding to dict,
				if tk.Frame, assign frame to Details frame.

		Raises:
			ValueError: wrong type of frame.
		"""
		if self.log: print("\nSet details_frame")
		if frame == None:
			# Generate a empty frame
			self.details_frame = tk.Frame(self.mid_frame)
		elif type(frame) == dict:
			# Generate frame accroding to a dict
			self.details_frame = tk.Frame(self.mid_frame,frame)
		elif type(frame) == tk.Frame:
			# Directly assign a frame
			self.details_frame = frame
		else:
			raise ValueError("You should input None or dict or class Frame.")

	def set_attributes_frame(self,frame=None):
		""" Set Attributes Frame 

		Args:
			frame (None or tk.Frame or dict, optional):
				Set bar_frame, if None, set Attributes frame null,
				if dict, set Attributes frame accroding to dict,
				if tk.Frame, assign frame to Attributes frame.

		Raises:
			ValueError: wrong type of frame.
		"""
		if self.log: print("\nSet attributes_frame")
		if frame == None:
			# Generate a empty frame
			self.attributes_frame = tk.Frame(self.mid_frame)
		elif type(frame) == dict:
			# Generate frame accroding to a dict
			self.attributes_frame = tk.Frame(self.mid_frame,frame)
		elif type(frame) == tk.Frame:
			# Directly assign a frame
			self.attributes_frame = frame
		else:
			raise ValueError("You should input None or dict or class Frame.")

	def set_logs_frame(self,frame=None):
		""" Set Logs Frame 
		
		Args:
			frame (None or tk.Frame or dict, optional):
				Set bar_frame, if None, set Logs frame null,
				if dict, set Logs frame accroding to dict,
				if tk.Frame, assign frame to Logs frame.

		Raises:
			ValueError: wrong type of frame.
		"""
		if self.log: print("\nSet logs_frame")
		if frame == None:
			# Generate a empty frame
			self.logs_frame = tk.Frame(self.base_frame)
		elif type(frame) == dict:
			# Generate frame accroding to a dict
			self.logs_frame = tk.Frame(self.base_frame,frame)
		elif type(frame) == tk.Frame:
			# Directly assign a frame
			self.logs_frame = frame
		else:
			raise ValueError("You should input None or dict or class Frame.")

	def pack(self):
		""" Pack for DesktopFrame """
		self.base_frame.pack(fill='both',expand=1)
		self.bar_frame.pack(side='top',fill='x')
		self.mid_frame.pack(side='top',fill='x')
		self.files_frame.pack(side='left',fill='y',expand=1)
		self.details_frame.pack(side='left',fill='both',expand=1)
		self.attributes_frame.pack(side='right',fill='y',expand=1)
		self.logs_frame.pack(side='bottom',fill='x')

	def pack_forget(self):
		""" Pack forget for DesktopFrame """
		for child_frame in ["bar_frame","files_frame",\
			"details_frame","attributes_frame","logs_frame"]:
				exec('self.{}.pack_forget()'.format(child_frame)) 

	def destory():
		""" Destory for DesktopFrame """
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


class FunctionalBlock():
	""" Components Tip and Components pair
	for example, a combobox with combobox name,
	an extry with extry content, etc.
	"""
	'''
	def __init__(self,master,text,*args,items=[''],locked=True,kind='select',current=0,reduce_=0,key=None):
		# 设置与主窗口
		self.sd = args[0]
		self.cd = args[1]
		self.master = master
		self.kind = kind
		self.key = key
		# 创建内容
		# 创建 - 框架
		self.frame = tk.Frame(self.window,bg=self.cd['back'],width=self.sd['rwidth'])
		# 创建 - 提示标语
		if type(text) == list:
			text = text[self.sd['language_id']]
		self.label = tk.Label(self.frame,text=text, width=int(self.sd['rletter']*2/5)-reduce_,\
			fg=self.cd['front'],bg=self.cd['back'],font=(self.sd['font'],self.sd['size']))
		# 创建 - 复选框类型
		if self.kind == 'select':
			self.combobox = ttk.Combobox(self.frame, width=int(self.sd['rletter']*3/5-1),font=(self.sd['font'],self.sd['size']))
			self.combobox['values'] = (items) # 设置下拉列表的值
			self.combobox.current(current)    # 设置下拉列表默认显示的值
			if locked: self.combobox.configure(state="readonly") # 不可编辑
		# 创建 - 输入框类型
		elif self.kind == 'entry':
		    self.entry = tk.Entry(self.frame,bg=self.cd['back'],fg=self.cd['front'],\
		    	font=(self.sd['font'],self.sd['size']),width=int(self.sd['rletter']*3/5))

	def pack(self):
		""" 安放基本控件 """
		self.frame.pack()
		if self.kind == 'select':
			self.combobox.pack(side='right')
		elif self.kind == 'entry':
			self.entry.pack(side='right')
		self.label.pack(side='right')

	def pack_forget(self):
		""" 隐藏基本控件 """
		self.frame.pack_forget()
		if self.kind == 'select':
			self.combobox.pack_forget()
		elif self.kind == 'entry':
			self.entry.pack_forget()
		self.label.pack_forget()

	def destroy(self):
		""" 销毁基本控件 """
		self.frame.destroy()
		if self.kind == 'select':
			self.combobox.destroy()
		elif self.kind == 'entry':
			self.entry.destroy()
		self.label.destroy()

	def bind(self,str_,fun_):
		""" 复选框的bind """
		self.combobox.bind(str_,fun_)

	def current(self,x=None):
		""" 复选框的current """
		return self.combobox.current(x)

	def set_value(self,x):
		""" 复选框的[value] """
		self.combobox['values'] = x

	def get_key_value_pair(self):
		""" 获取键值对 """
		if self.kind == 'entry':
			return {self.key:eval(self.entry.get())}
		else:
			return {self.key:eval(self.combobox.get())}
	'''


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
	id_: (str) An ID of a page. When you set Combobox 
		to flip child pages, id_ of child pages show
		in the combobox.
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

	functioin summary:

	_update_child_page_id()

	__init__()
	__str__()

	set_current()
	pack_current()

	"""
	def __init__(self, master, cnf={}, **kw):
		""" Create a Page
		Page can have 'components' and 'child pages'.
		We can set a 'combobox' to flip child pages.
		"""
		# Get master
		self.master = master

		# Get page components
		if "child_page" in kw:
			self.set_child_page()
		self.page_member = []

		# get page back to
		if "back" in kw:
			self.set_back(kw["back"])
		else:
			self.back = None

		# Get Child Pages 
		self.child_page = []
		if "child_page" in kw:
			if type(kw["child_page"]) == list:
				self.child_page = kw["child_page"]
			else:
				self.child_page = None

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
			self.flip = 'Tree'

		# whether to pack a page
		if ("pack_way" not in kw) or (kw["pack_way"] == None):
			# Do not have child page
			self.pack_way = None
		else:
			self.pack_way = kw["pack_way"]

	def __str__(self):
		""" """
		return "Page: "+str(self.id_)

	def set_child_page(self,child_page,place=-1):
		"""
		@author 每天1990
		@desc 本模块是一个测试文件，用来说明pydoc的读取内容
		@date 2017/4/13
		说明：
		classes:testclass()，具有function1()和function2()两个方法

		function：test1()，test2()，test3()

		Data：a，b
		"""
		""" Set child pages 

		You can whether input a page list or
		add into a certain place (like append)
		
		Args:
			..

		Returns:
			..

		Raises:
			..
		"""
		if type(child_page) == Page:
			if len(self.child_page) > 0:
				self.child_page.append(place)
		elif type(child_page) == list:
			for item in child_page:
				if type(child_page) != Page:
					raise ValueError("child_page should be Page or Page List")
			self.child_page = child_page
		else:
			raise ValueError("child_page should be Page or Page List")



	def set_back(self,back_page):
		""" Set back to page"""
		if type(back_page) != Page:
			print("You should input a back to Page!")
			return False
		self.back_page = back_page

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
		""" """
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

