import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy.stats import kde


def plot_hist2d(samples, x_limits, y_limits, nbins=300, title=None, file_name=None, **kwargs):
    """
    The function plots 2d histogram for given samples
    :param samples: numpy array
    :param x_limits:
    :param y_limits:
    :param nbins:
    :param title:
    :param file_name: file name (if not provided, we dont save the picture)
    :param kwargs: arguments for plt.figure
    :return:
    """
    plt.close()
    plt.figure(**kwargs)

    x = samples[:, 0]
    y = samples[:, 1]
    k = kde.gaussian_kde([x, y], bw_method=0.1)
    xi, yi = np.mgrid[x_limits[0]:x_limits[1]:nbins * 1j, y_limits[0]:y_limits[1]:nbins * 1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))

    # Make the plot
    plt.pcolormesh(xi, yi, zi.reshape(xi.shape))
    plt.axis('off')
    plt.xlim((x_limits[0], x_limits[1]))
    plt.ylim((y_limits[0], y_limits[1]))
    if title is not None:
        plt.title(title)
    plt.tight_layout()
    if file_name is not None:
        plt.savefig(file_name, format='png')
    plt.show()


def plot_contours(target, x_limits, y_limits, npts=250, num_lines=6, device="cpu", **kwargs):
    plt.close()
    plt.figure(**kwargs)
    xside = np.linspace(-x_limits[0], x_limits[1], npts)
    yside = np.linspace(-y_limits[0], y_limits[1], npts)
    xx, yy = np.meshgrid(xside, yside)
    z = torch.tensor(np.hstack([xx.reshape(-1, 1), yy.reshape(-1, 1)]), dtype=torch.float32, device=device)
    log_probs = target.log_prob(z=z).cpu().detach().numpy()
    p = np.exp(log_probs).reshape(npts, npts)
    plt.contour(xx, yy, p, num_lines, colors='k')
    plt.axis('equal')
