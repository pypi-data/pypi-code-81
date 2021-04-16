import numpy as np

import nptdms
import imageio

def read_tdms_video(file):
    """
    Read TDMS video file.
    
    Arguments:
        file (string): The path to the TDMS file.
    Returns:
        images (2D array): The image series data. 
        metadata (pandas DataFrame): A pandas DataFrame with the metadata. 
    """
    
    tdms_file = nptdms.TdmsFile(file)
    p = tdms_file.properties 
    
    dimx = int(p['dimx'])
    dimy = int(p['dimy'])
    frames = int(p['dimz'])
    exposure = float(p['exposure'])
    binning = int(p['binning'])

    metadata = {
        "dimx": dimx,
        "dimy": dimy,
        "frames": frames,
        "exposure": exposure,
        "binning": binning,
        }
    
    images = tdms_file['Image']['Image'].data
    return images.reshape(frames, dimx, dimy), metadata


def read_tiff_stack(file):
    """
    Read TIFF stack file.
    
    Arguments:
        file (string): The path to the TIFF file.
    Returns:
        images (2D array): The image series data. 
        metadata (pandas DataFrame): A pandas DataFrame with the metadata. 
    """
    images = io.imread(file)
    frames = images.shape[0]
    dimy = images.shape[1]
    dimx = images.shape[2]
    metadata = {
        "dimx": dimx,
        "dimy": dimy,
        "frames": frames,
        }
    return images, metadata       

  
def read_mp4_video(file):
    """
    Read MP4 video file.
    
    Arguments:
        file (string): The path to the TIFF file.
    Returns:
        images (2D array): The image series data. 
        metadata (pandas DataFrame): A pandas DataFrame with the metadata. 
    """
    
    video = imageio.get_reader(file)
    dimx = video.get_meta_data()['size'][0]
    dimy = video.get_meta_data()['size'][1]
    frames = video.count_frames()
    images = np.stack([video.get_data(i)[:,:,0] for i in range(frames)])
    metadata = {
        "dimx": dimx,
        "dimy": dimy,
        "frames": frames,
        }
    return images, metadata
