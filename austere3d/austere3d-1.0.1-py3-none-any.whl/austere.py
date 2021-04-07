#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ =  '1.0.1'

import sys
assert sys.version_info >= (3, 6)
import numpy as np

##############################################################################

def generate_austere(depthmap, wallpaper, d_invert, d_factor, symmetry,
                     progress_var=False, popup=False):
    if (len(depthmap.shape)>2):
        return 'depthmap is probably not a greyscale image'
    if (wallpaper.shape[2]==4):
        # remove transparency layer:
        wallpaper = wallpaper[:,:,0:3]
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

def make_austere(depthmapfile, wallpaperfile, d_invert, d_factor, symmetry,
                 progress_var=False, popup=False, outputfile='output/austere.png'):
    import matplotlib.pyplot as plt

    depth = plt.imread(depthmapfile)

    # imread scaled [0...255] to [0...1] so it must be rescaled back
    wallpaper = 256*plt.imread(wallpaperfile)
    
    austere = generate_austere(depth, wallpaper, d_invert, d_factor,
                               symmetry, progress_var, popup)

    if(isinstance(austere, str)):
        # an error string was returned
        return austere
    else:
        plt.imsave(outputfile, austere.astype(float)/256)    

##############################################################################

if __name__ == '__main__':

    ### DEPTHMAP ###
    #depthmapfile = 'blackhole'
    #depthmapfile = 'bumps'
    depthmapfile = 'cube'
    #depthmapfile = 'donut'
    #depthmapfile = 'ic'
    #depthmapfile = 'rings'
    #depthmapfile = 'ripples'
    #depthmapfile = 'shark'
    #depthmapfile = 'sombrero'
    #depthmapfile = 'upanddown'
    #depthmapfile = 'vortex'

    ### WALLPAPER ###
    #wallpaperfile = 'birds'
    #wallpaperfile = 'citrus'
    #wallpaperfile = 'clouds'
    #wallpaperfile = 'coffee'
    #wallpaperfile = 'flowers'
    #wallpaperfile = 'fruit'
    #wallpaperfile = 'hieroglyphs'
    #wallpaperfile = 'houses'
    #wallpaperfile = 'ink_splashes'
    wallpaperfile = 'quilt'
    #wallpaperfile = 'quilt_drops'
    #wallpaperfile = 'school'
    #wallpaperfile = 'underwater_world'
    #wallpaperfile = 'water'

    ### OPTIONS ###
    d_invert = False # invert up and down
    d_factor = 0.25  # 0...1
    symmetry = 0.5   # 0...1

    print(f'\nCreating an autostereogram from the depthmap "{depthmapfile}"')
    print(f'and the wallpaper "{wallpaperfile}"...\n')

    returncode = make_austere('depthmap/'+depthmapfile+'.png',
                              'wallpaper/'+wallpaperfile+'.png',
                              d_invert,
                              d_factor,
                              symmetry)
    if (returncode):
        print(f'ERROR: {returncode}')
    else:
        print('The image file "output/austere.png" has been created.\n')
