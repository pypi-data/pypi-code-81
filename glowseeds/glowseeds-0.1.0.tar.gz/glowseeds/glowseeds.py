import skimage.io
import skimage.feature
import skimage.filters
import skimage.util
import skimage.segmentation
from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage as ndi
import skimage.color
import skimage.morphology
from skimage import measure
import pandas as pd
import os

def load_pair(bf_img_f, fl_img_f):
    ims = [skimage.io.imread(i) for i in [bf_img_f, fl_img_f] ]
    return [skimage.util.img_as_ubyte(skimage.color.rgb2gray(i)) for i in ims]

def threshold(img, lower=25, upper=100):
    topped = img < upper
    tailed = img > lower
    return np.logical_and(topped,tailed)

def plot(img, title="blank"):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(img, cmap=plt.cm.gray)
    ax.set_title(title)
    ax.axis('off')
    plt.show()

def pixel_values(img_fname):
    img = skimage.io.imread(img_fname)
    img = skimage.util.img_as_ubyte(skimage.color.rgb2gray(img))
    return img.ravel()

def watershed(img, compactness=0, min_distance=30): #binary thresholded image
    ## remove small and large objects before getting here!!!
    ##min distance is the important parameter for splitting overlapping objects

    distance = ndimage.distance_transform_edt(img)
    coords = skimage.feature.peak_local_max(distance, footprint=np.ones((3, 3)), labels=img, min_distance=min_distance)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)
    labels = skimage.segmentation.watershed(-distance, markers, mask=img, compactness=compactness)
    return labels

def plot_jellybeans(labels, title='Identified objects', bg_image=None, fname=None):
    fig, ax= plt.subplots(figsize=(4, 3))
    ax.imshow(skimage.color.label2rgb(labels,image=bg_image, bg_label=0))
    ax.set_title(title)
    plt.savefig(fname,dpi=240)

def desalt(img, disk_size=12):
    selem = skimage.morphology.disk(disk_size)
    return skimage.morphology.opening(img, selem)

def is_small_and_fat(obj, major_to_minor: int = 2,
                      min_area: int = 100 * 60):
    try:
        ratio = obj.major_axis_length / obj.minor_axis_length
        if ratio <= major_to_minor and obj.area <= min_area:
            return True
        else:
            return False
    except ZeroDivisionError:
        return None

def clear_filtered_labels(label_img, rprops):
    keep = [r.label for r in rprops]
    return np.isin(label_img, keep) * label_img

def to_pandas(regions, bf_filename, fl_filename, ol_fname):

    data = {
        "seed_number" : list(range(1,len(regions)+1)),
        "seed_label" : [r.label for r in regions],
        "mean_intensity" : [np.mean(r.intensity_image) for r in regions],
        "original_brightfield" : [bf_filename] * len(regions),
        "original_fluorescence" : [fl_filename] * len(regions),
        "objects_preview" : [ol_fname] * len(regions)
    }

    return pd.DataFrame(data)

def make_overlay_fname(dir, bf_filename):
    if dir is None:
        dir = ""
    return os.path.join(dir, os.path.splitext(bf_filename)[0] + "_objects.jpg")

def do(bf_filename,fl_filename,
       disk_size = 12,
       threshold_min = 25,
       threshold_max = 100,
       compactness = 0,
       min_distance = 30,
       width_to_length = 2,
       min_area = 100 * 60,
       figure_directory  = None
       ):
    bf, fl = load_pair(bf_filename,fl_filename)
    overlay_fname = make_overlay_fname(figure_directory, bf_filename)
    ds_img = desalt(bf, disk_size=disk_size)
    bin = threshold(ds_img, threshold_min, threshold_max)
    labels = watershed(bin, compactness=compactness, min_distance=min_distance)
    props = skimage.measure.regionprops(labels, intensity_image=fl)
    filtered_props = [r for r in props if is_small_and_fat(r, major_to_minor=width_to_length, min_area = min_area) ] ## make sure user can set values for small and fat
    filtered_labels = clear_filtered_labels(labels, filtered_props)
    plot_jellybeans(filtered_labels, fname= overlay_fname, title=bf_filename, bg_image=bf)
    return to_pandas(filtered_props, bf_filename, fl_filename, overlay_fname)


