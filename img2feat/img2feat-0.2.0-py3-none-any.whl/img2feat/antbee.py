# https://aidiary.hatenablog.com/entry/20180217/1518833659
# https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

import cv2
import numpy as np
import urllib.request
import os
import zipfile
import glob
import hashlib
import shutil

from img2feat import CNN

str = ['ant', 'bee']

def load_hymenoptera( root ):
    filename = 'hymenoptera_data.zip'
    url = 'https://download.pytorch.org/tutorial/'+filename

    dir = os.path.join( root, 'ant-vs-bee' )
    os.makedirs( dir, exist_ok=True )
    dir_filename = os.path.join( dir, filename )

    download = False
    if( os.path.exists( dir_filename ) ):
        with open( dir_filename, 'rb' ) as fin:
            md5 = hashlib.md5( fin.read() ).hexdigest()
        if( md5 != '5f8c32a6554f6acb4d649776e7735e48' ):
            download = True
    else:
        download = True

    if( download ):
        urllib.request.urlretrieve(url, dir_filename)

    extract = False
    nb_files = [124, 121, 70, 83]
    dirs = ['train/ants/*', 'train/bees/*', 'val/ants/*', 'val/bees/*']
    for n, d in zip( nb_files, dirs ):
        files = glob.glob( os.path.join( dir, 'hymenoptera_data/'+d ) )
        if( len(files) != n ):
            extract = True

    if( extract ):
        if( os.path.exists( os.path.join( dir, 'hymenoptera_data' ) ) ):
            shutil.rmtree( os.path.join( dir, 'hymenoptera_data' ) )
        with zipfile.ZipFile(dir_filename) as existing_zip:
            existing_zip.extractall( dir )

def load_imgs( dir ):
    keys = [ 'train0', 'train1', 'test0', 'test1' ]
    dirs = ['train/ants/*', 'train/bees/*', 'val/ants/*', 'val/bees/*']
    data = {}

    for k,d in zip(keys, dirs):
        data[k] = []
        files = glob.glob( os.path.join( dir, d ) )
        files.sort()
        for file in files:
            img = cv2.imread( file )
            if( img is not None ):
                data[k].append( img )

    Xtrain = data['train0'] + data['train1']
    Ytrain = np.concatenate( (np.zeros( (len(data['train0']),), dtype=np.int ),
                              np.ones ( (len(data['train1']),), dtype=np.int ) ),
                              axis=0 )
    Xtest = data['test0'] + data['test1']
    Ytest = np.concatenate( (np.zeros( (len(data['test0']),), dtype=np.int ),
                             np.ones ( (len(data['test1']),), dtype=np.int ) ),
                              axis=0 )

    return (Xtrain, Ytrain), (Xtest, Ytest)


def extract_squared_imgs( dir ):
    org_dir = os.path.join( dir, 'hymenoptera_data' )
    sqr_dir = os.path.join( dir, 'hymenoptera_squared' )

    keys = [ 'train0', 'train1', 'test0', 'test1' ]
    dirs = ['train/ants/', 'train/bees/', 'val/ants/', 'val/bees/']

    extract = False
    nb_files = [29, 36, 18, 26]
    for n, d in zip( nb_files, dirs ):
        files = glob.glob( os.path.join( dir, 'hymenoptera_squared/'+d+'*' ) )
        if( len(files) != n ):
            extract = True

    if( extract ):
        if( os.path.exists(sqr_dir ) ):
            shutil.rmtree( sqr_dir )

        for k,d in zip(keys, dirs):
            dst_dir = os.path.join( sqr_dir, d )
            os.makedirs( dst_dir )
            files = glob.glob( os.path.join( org_dir, d )+'*' )
            files.sort()
            for file in files:
                img = cv2.imread( file )
                if( img is not None ):
                    height, width, _ = img.shape
                    ratio = height / width
                    if( ratio > 0.75 and ratio < 1.25 ):
                        if height >= width:
                            cropped_img = img[ int(height/2-width/2):int(height/2+width/2), :, : ]
                        else:
                            cropped_img = img[ :, int(width/2-height/2):int(width/2+height/2), : ]

                        img = cv2.resize( cropped_img, (256,256) )
                        dst_file = os.path.join( dst_dir, os.path.basename(file) )
                        cv2.imwrite( dst_file, img )

def load( squared=True, root=None ):
    if( root is None ):
        root = os.path.dirname(__file__)
    load_hymenoptera( root )

    dir = os.path.join( root, 'ant-vs-bee' )
    if( squared ):
        extract_squared_imgs( dir )
        dir = os.path.join( dir, 'hymenoptera_squared' )
    else:
        dir = os.path.join( dir, 'hymenoptera_data' )

    return load_imgs( dir )

def load_squared_npy( name, root=None ):
    if( root is None ):
        root = os.path.dirname(__file__)

    dir = os.path.join( root, 'ant-vs-bee/hymenoptera_squared' )
    dir_filename = os.path.join( dir, name+'.npz' )

    if( not os.path.exists( dir_filename ) ):
        (Xtrain, Ytrain), (Xtest, Ytest) = load( True, root )
        cnn = CNN(name)
        Xtrain = cnn( Xtrain )
        Xtest = cnn( Xtest )
        np.savez( dir_filename, Xtrain=Xtrain, Ytrain=Ytrain, Xtest=Xtest, Ytest=Ytest )

    d = np.load( dir_filename )
    return (d['Xtrain'], d['Ytrain']), (d['Xtest'], d['Ytest'])

