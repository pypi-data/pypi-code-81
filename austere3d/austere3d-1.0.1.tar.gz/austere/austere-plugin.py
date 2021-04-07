#!/usr/bin/env python
# python 2 syntax must be used here for gimp version <3
# -*- coding: utf-8 -*-

from gimpfu import *
import numpy as np

##############################################################################

def generate_austere(depthmap, wallpaper, d_invert, d_factor, symmetry,
                     progress_var=False, popup=False):
    h_depthmap  = depthmap.shape[0]  # height of depthmap
    w_depthmap  = depthmap.shape[1]  # width  of depthmap
    h_wallpaper = wallpaper.shape[0] # height of wallpaper
    w_wallpaper = wallpaper.shape[1] # width  of wallpaper
    idx = np.zeros(w_depthmap + w_wallpaper)
    # w_austere is a little bit larger than w_depthmap:
    w_austere = w_depthmap + int(w_wallpaper * (1-d_factor))
    austere = np.zeros((h_depthmap, w_austere, 3), dtype=np.int)
    for iy in range(h_depthmap): # loop over all lines in depthmap
        if progress_var:
            progress_var.set(int(1+100*iy/h_depthmap))
            popup.update_idletasks()
        for ix in range(w_wallpaper): # start by copying original wallpaper
            idx[ix] = ix
        d_old = w_wallpaper
        for ix in range(w_depthmap): # loop over all columns in current line
            if d_invert: # inverted depthmap?
                depthmap[iy,ix] = 1. - depthmap[iy,ix]
            d = int((1. - d_factor * depthmap[iy,ix]) * w_wallpaper)
            idx[ix+d] = idx[ix]
            if (d > d_old): # regenerate dismembered wallpaper?
                for i in range(d-d_old):
                    idx[ix+d-i-1] = (idx[ix]+w_wallpaper-i-1) % w_wallpaper
            d_old = d
        for ix in range(w_austere):
            idx_shifted = int((idx[ix] - idx[int(symmetry*w_austere)] +
                               w_wallpaper) % w_wallpaper)
            austere[iy,ix,:] = wallpaper[iy % h_wallpaper,idx_shifted,:]
    return austere

##############################################################################

def main_plugin(wallpaper, depthmap, d_invert, d_factor_percent, symmetry_percent):
    symmetry = symmetry_percent/100
    d_factor = d_factor_percent/100
    # ----- wallpaper -----
    gimp.progress_init('Reading wallpaper...')
    wallpaper_array = np.zeros((wallpaper.height, wallpaper.width, 3))
    for x in range(wallpaper.width):
        gimp.progress_update(float(x) / float(wallpaper.width)) # progress bar
        for y in range(wallpaper.height):
            wallpaper_array[y,x,:] = wallpaper.get_pixel(x,y)[0:3]
    # ----- depthmap -----
    gimp.progress_init('Reading depthmap...')
    depthmap_array = np.zeros((depthmap.height, depthmap.width))
    for x in range(depthmap.width):
        gimp.progress_update(float(x) / float(depthmap.width)) # progress bar
        for y in range(depthmap.height):
            depthmap_array[y,x] = float(depthmap.get_pixel(x,y)[0])/256.
    # ----- austere -----
    austere = generate_austere(depthmap_array, wallpaper_array, d_invert, d_factor, symmetry)
    img = gimp.Image(austere.shape[1], austere.shape[0], wallpaper.type)
    destDrawable = gimp.Layer(img, 'austere', austere.shape[1], austere.shape[0],
                              wallpaper.type, wallpaper.opacity, wallpaper.mode)
    img.add_layer(destDrawable, 0)
    gimp.progress_init('Writing austere...')
    for iy in range(austere.shape[0]):
        gimp.progress_update(float(iy) / float(austere.shape[0])) # progress bar
        for ix in range(austere.shape[1]):
            destDrawable.set_pixel(ix,iy,austere[iy,ix,:])
    gimp.Display(img)
    destDrawable.flush()

##############################################################################

register(
    'austere', # window title
    'Create AUtoSTEREograms', # header in window
    'Create AUtoSTEREograms from depthmap and wallpaper', # help text
    'Rolf Sander', # author
    'Rolf Sander', # copyright
    '2017-2020', # date
    '<Image>/Filters/Render/Autostereogram...', # menu path
    '*', # imagetypes (*, RGB, RGB*, GRAY*, INDEXED, etc.)
    [
        (PF_DRAWABLE, 'wallpaper',         'wallpaper',         None),
        (PF_DRAWABLE, 'depthmap',          'Depthmap',          None),
        (PF_BOOL,     'd_invert',          'Invert?',           False),
        (PF_SLIDER,   'd_factor_percent',  'Depth factor in %', 25, (0, 100, 1)),
        (PF_SLIDER,   'symmetry_percent',  'Symmetry in %',     50, (0, 100, 1)),
    ], # params
    [], # results
    main_plugin, # function
    # Add empty value for menu here because it is already defined above.
    # The entry cannot be omitted, otherwise "main_plugin" produces two
    # more parameters for the function call.
    menu=''
    )

main()

##############################################################################

