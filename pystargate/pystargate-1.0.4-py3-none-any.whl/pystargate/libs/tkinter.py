#!/usr/bin/env python
# -*- coding:utf-8
import sys
if int( sys.version[0] ) == 3:
    import tkinter as tk
elif int( sys.version[0] ) == 2:
    import Tkinter as tk

class Tkinter():

    def TkinterDiv(self):
        return tk.Tk()


    def TkinterShowDiv(self,div):
        div.mainloop()


    def TkinterButton(self,_div,text,color1=None,color2=None,command=None,width=None,height=None,place=1):
        button=tk.Button(master=_div,text=text, bg=color1,activebackground=color2,command=command,width=width,height=height)
        if place==1:
            button.pack()
        elif place==2:
            button.grid()


    def TkinterLabel(self,_div,text,color=None,width=None,height=None,place=1):
        button=tk.Label(master=_div,text=text, bg=color,width=width,height=height)
        if place==1:
            button.pack()
        elif place==2:
            button.grid()

