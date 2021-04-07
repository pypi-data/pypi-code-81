#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
assert sys.version_info >= (3, 6)
# Tkinter gui:
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter import ttk # for progressbar
# other modules:
from PIL import Image, ImageTk
from austere import make_austere
import os # basename

about_text = '''Create AUtoSTEREograms
(c) Rolf Sander 2017-2020
http://www.rolf-sander.net'''

THUMBSIZE = 350
OUTPUTDIR = 'output'
WINDOWTITLE = 'AUtoSTEREogram'
INITIAL_DEPTHMAP  = 'cube.png'
INITIAL_WALLPAPER = 'birds.png'

def start_calc():
    d_factor = float(d_factor_percent.get())/100.
    symmetry = float(symmetry_percent.get())/100.
    popup = Toplevel()
    popup.title(WINDOWTITLE)
    progress_var = DoubleVar()
    progressbar = ttk.Progressbar(popup, variable=progress_var)
    progressbar.pack(padx=10, pady=10, fill=X)
    label1 = Label(popup, width=60, font='-weight bold', wraplength=500,
                   text='Please wait...')
    label1.pack(pady=10)
    popup.grab_set() # make main window inactive
    outputfile = OUTPUTDIR + '/austere_' + \
                 os.path.splitext(os.path.basename(depthmapfile))[0] + \
                 '_' + os.path.splitext(os.path.basename(wallpaperfile))[0] + '.png'
    returncode = make_austere(depthmapfile, wallpaperfile, d_invert.get(),
                              d_factor, symmetry, progress_var, popup, outputfile)
    if (returncode):
        label1['text'] = 'ERROR: %s' % (returncode)
    else:
        label1['text'] = 'The file %s has been created.' % (outputfile)
        # show austere image:
        austerepic = Button(popup, height=300, width=500)
        austerepic.pack()
        img0 = Image.open(outputfile)
        w = img0.width
        h = img0.height
        fct = min(1,float(THUMBSIZE)/max(w, h)) # scalefactor
        img0 = img0.resize((int(w*fct), int(h*fct)), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img0)
        austerepic.image = img1
        austerepic.config(image=img1)
    # OK button:
    okbutton = Button(popup, text='OK', font='-weight bold', command=popup.destroy)
    okbutton.pack(pady=10)
    
def show_wallpaperfile():
    img0 = Image.open(wallpaperfile)
    w = img0.width
    h = img0.height
    fct = min(1,float(THUMBSIZE)/max(w, h)) # scalefactor
    img0 = img0.resize((int(w*fct), int(h*fct)), Image.ANTIALIAS)
    img1 = ImageTk.PhotoImage(img0)
    wallpaperpic.image = img1
    wallpaperpic.config(image=img1)
    wallpaperfilelabel.config(
        font='-weight bold',
        text='Wallpaper: '+os.path.basename(wallpaperfile)+' ('+str(w)+'x'+str(h)+')')
    
def get_wallpaperfile():
    global wallpaperfile
    new_wallpaperfile = filedialog.askopenfilename(
        title = 'Select a wallpaper file',
        initialdir = 'wallpaper',
        initialfile = INITIAL_WALLPAPER,
        filetypes = [('pic files', '.png .jpg'), ('all files', '.*')])
    if (file_check(new_wallpaperfile, 3)):
        wallpaperfile = new_wallpaperfile
    else:
        popup = Toplevel()
        popup.title(WINDOWTITLE)
        Label(popup, text='Error: Choose another wallpaper file',
              fg='red', font='-weight bold').pack(padx=20, pady=20)
        Button(popup, text='OK', font='-weight bold',
               command=popup.destroy).pack(padx=20, pady=20)
        popup.grab_set() # make main window inactive
    show_wallpaperfile()
    
def show_depthmapfile():
    img0 = Image.open(depthmapfile)
    w = img0.width
    h = img0.height
    fct = min(1,float(THUMBSIZE)/max(w, h)) # scalefactor
    img0 = img0.resize((int(w*fct), int(h*fct)), Image.ANTIALIAS)
    img1 = ImageTk.PhotoImage(img0)
    depthmappic.image = img1
    depthmappic.config(image=img1)
    depthmapfilelabel.config(
        font='-weight bold',
        text='Depthmap: '+os.path.basename(depthmapfile)+' ('+str(w)+'x'+str(h)+')')

def get_depthmapfile():
    global depthmapfile
    new_depthmapfile = filedialog.askopenfilename(
        title = 'Select a depthmap file',
        initialdir = 'depthmap',
        initialfile = INITIAL_DEPTHMAP,
        filetypes = [('pic files', '.png .jpg'), ('all files', '.*')])
    if (file_check(new_depthmapfile, 1)):
        depthmapfile = new_depthmapfile
    else:
        popup = Toplevel()
        popup.title(WINDOWTITLE)
        Label(popup, text='Error: Choose another depthmap file',
              fg='red', font='-weight bold').pack(padx=20, pady=20)
        Button(popup, text='OK', font='-weight bold',
               command=popup.destroy).pack(padx=20, pady=20)
        popup.grab_set() # make main window inactive
    show_depthmapfile()

def file_check(filename, colors):
    if (not os.path.isfile(filename)):
        return False    
    # qqq
    # if (not correct colordepth(filename, colors)):
    #     return False    
    return True
    
def popupwindow_about():
    popup = Toplevel()
    popup.title(WINDOWTITLE)
    label1 = Label(popup, font='-weight bold', text=about_text)
    label1.pack(padx=20)
    Button(popup, text='OK', font='-weight bold',
           command=popup.destroy).pack(pady=20)
    popup.grab_set() # make main window inactive

gui = Tk()
gui.title(WINDOWTITLE)

wallpaperfile = 'wallpaper/' + INITIAL_WALLPAPER
wallpaperpic = Button(height=THUMBSIZE, width=THUMBSIZE, command=get_wallpaperfile)
wallpaperpic.grid(padx=20, pady=20, row=0, column=0, columnspan=2)

depthmapfile = 'depthmap/' + INITIAL_DEPTHMAP
depthmappic = Button(height=THUMBSIZE, width=THUMBSIZE, command=get_depthmapfile)
depthmappic.grid(padx=20, pady=20, row=0, column=2, columnspan=2)

wallpaperfilelabel = Label(gui)
wallpaperfilelabel.grid(row=1, column=0, columnspan=4)
show_wallpaperfile()

depthmapfilelabel = Label(gui)
depthmapfilelabel.grid(row=2, column=0, columnspan=4)
show_depthmapfile()

d_invert = BooleanVar()
Checkbutton(gui, text='Invert Depthmap?', font='-weight bold',
            variable=d_invert).grid(pady=10, row=3, column=0, columnspan=4)

d_factor_percent = Scale(gui, from_=0, to=100, orient=HORIZONTAL,
                         length=400, font='-weight bold', label='Depth Factor in %:')
d_factor_percent.grid(pady=10, row=4, column=0, columnspan=4)
d_factor_percent.set(15)

symmetry_percent = Scale(gui, from_=0, to=100, orient=HORIZONTAL,
                         length=400, font='-weight bold', label='Symmetry in %:')
symmetry_percent.grid(pady=10, row=5, column=0, columnspan=4)
symmetry_percent.set(50)

Button(gui, text='About', font='-weight bold',
       command=popupwindow_about).grid(pady=20, row=6, column=0)
Button(gui, text='Create AUtoSTEREogram', font='-weight bold',
       command=start_calc).grid(pady=20, row=6, column=1, columnspan=2)
Button(gui, text='Quit', font='-weight bold',
       #fg='red',
       command=quit).grid(pady=20, row=6, column=3)

mainloop()
