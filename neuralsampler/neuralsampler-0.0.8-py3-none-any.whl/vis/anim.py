# create the animation to show the learning


import os

# plots the animation
import numpy as np
from matplotlib import pyplot as plt
plt.rcParams["image.cmap"] = 'viridis'
plt.rcParams["text.usetex"] = 'False'
from celluloid import Camera
from pylab import meshgrid
from sysflow.utils.common_utils.file_utils import load
from tqdm.contrib import tzip

from neuralsampler.models.dw import Doublewell
from neuralsampler.models.gaussian import Gaussian
from neuralsampler.models.mb import MuellerPotential

MODEL = {"mb": MuellerPotential, "dw": Doublewell, "gaussian": Gaussian}

# probably can merged into a class
def generate_anim(args):
    # generate animation of the learning process

    # choice: gaussian, dw, mb

    #region unpack the params
    model = args.model
    dim = args.dim
    G_loss = args.G_loss
    exp_dir = args.exp_dir
    #endregion

    md = MODEL[model](dim=dim)


    # plot the reference
    d = 2

    xmin = -2
    xmax = 1
    ymin = -0.5
    ymax = 2.5

    dx = 0.04
    x = np.arange(xmin, xmax, dx)
    y = np.arange(ymin, ymax, dx)
    nx = x.shape[0]
    ny = y.shape[0]
    X, Y = meshgrid(x, y)  # grid of point
    xg = np.zeros((nx * ny, d))
    xg[:, 0] = np.reshape(X, (nx * ny))
    xg[:, 1] = np.reshape(Y, (nx * ny))
    Z_ref = np.reshape(md.energy(xg), (ny, nx))
    X_ref = X
    Y_ref = Y
    Z_ref = np.exp(-Z_ref)

    # vis directary
    vis_dir = os.path.join(exp_dir, "vis")
    fname = "{}_d{}.pkl".format(model, dim)
    fname = os.path.join(vis_dir, fname)
    sample_dict = load(fname)

    if 'GAN' in G_loss: 
        if model == 'mb': 
            fig, axes = plt.subplots(3, 3, figsize=(6.4 * 3, 4.8))
        else: 
            fig, axes = plt.subplots(1, 3, figsize=(6.4 * 3, 4.8))
    else: 
        fig, axes = plt.subplots(1, 2, figsize=(6.4 * 2, 4.8))

    camera = Camera(fig)

    X_list = sample_dict["X"]
    Y_list = sample_dict["Y"]
    Z_list = sample_dict["Z"]
    if 'GAN' in G_loss: 
        D_list = sample_dict["D"]
    else: 
        # placeholder here
        D_list = sample_dict["Z"]

    if model == 'mb': 
        for XX, YY, ZZ, DD in tzip(X_list, Y_list, Z_list, D_list):
            for i in range(3): 
                X = XX[i]
                Y = YY[i]
                Z = ZZ[i]
                D = DD[i]

                ax = axes[i, 0]
                ax.contourf(X, Y, Z)

                ax = axes[i, 1]
                if model == 'mb': 
                    ax.contourf(X_ref, Y_ref, Z_ref)
                elif model == 'dw': 
                    Z_ref = np.exp( - 0.045 * X ** 4 + X ** 2 - 0.5 * Y ** 2)
                    ax.contourf(X, Y, Z_ref)

                if 'GAN' in G_loss: 
                    ax = axes[i, 2]
                    ax.contourf(X, Y, D)
                    
            camera.snap()
    else: 
        for X, Y, Z, D in tzip(X_list, Y_list, Z_list, D_list):
            ax = axes[0]
            ax.contourf(X, Y, Z)

            ax = axes[1]
            if model == 'mb': 
                ax.contourf(X_ref, Y_ref, Z_ref)
            elif model == 'dw': 
                Z_ref = np.exp( - 0.045 * X ** 4 + X ** 2 - 0.5 * Y ** 2)
                ax.contourf(X, Y, Z_ref)

            if 'GAN' in G_loss: 
                ax = axes[2]
                ax.contourf(X, Y, D)

            camera.snap()

    animation = camera.animate()

    fname = "{}_d{}.mp4".format(model, dim)
    fname = os.path.join(vis_dir, fname)
    animation.save(fname)
