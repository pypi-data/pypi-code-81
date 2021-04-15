import sys
import os
import os.path
import cv2

#from PIL import Image, ImageDraw
#import matplotlib.pyplot as plt
import importlib.util
import numpy as np
import math
import uuid


from sklearn import neighbors
import pickle

from srgan_krasserm.model import resolve_single
from srgan_krasserm.model.srgan import generator, discriminator
from srgan_krasserm.train import SrganTrainer, SrganGeneratorTrainer
from srgan_krasserm import utils


from threading import Thread
import time 
import re
import dlib

pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
else:
    from tensorflow.lite.python.interpreter import Interpreter

import face_recognition_models

predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
pose_predictor = dlib.shape_predictor(predictor_68_point_model)

def load_image(path) :
    image = cv2.imread(path)
    
    return image

def load_model(model_path=None):
    if model_path is None:
        raise Exception("Must supply face detection classifier")
        
    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def load_knn(model_path=None) :
    if model_path is None:
        raise Exception("Must supply knn classifier")

    with open(model_path, 'rb') as f:
        knn_clf = pickle.load(f)
    return knn_clf 



def _css_to_rect(css):
    """
    Convert a tuple in (top, right, bottom, left) order to a dlib `rect` object
    :param css:  plain tuple representation of the rect in (top, right, bottom, left) order
    :return: a dlib `rect` object
    """
    return dlib.rectangle(css[0], css[1], css[2], css[3])


def _raw_face_landmarks(face_image, face_locations):
    face_locations = [_css_to_rect(face_location) for face_location in face_locations]
    
    return [pose_predictor(face_image, face_location) for face_location in face_locations]



def face_locations(image, threshold=0.8) :
    """
    :param model_name: path to saved model on disk
    :param image        : request image for searching faces
    :param threshold    : (optional) face detection threshold
    """
    imgH, imgW, channel = image.shape 
    
    # Open Model
    CWD_PATH =  os.path.dirname(os.path.abspath(__file__))
    PATH_TO_CKPT = os.path.join(CWD_PATH, 'detection', 'face.tflite')
    model = load_model(PATH_TO_CKPT)
    input_details    = model.get_input_details()
    output_details  = model.get_output_details()
    floating_model = (input_details[0]['dtype'] == np.float32)
    height            = input_details[0]['shape'][1]
    width             = input_details[0]['shape'][2]

    # Prepare Image
    frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height))
    
    input_data = np.expand_dims(frame_resized, axis=0)
    
    # Push Data
    if floating_model:
        input_mean = 127.5
        input_std = 127.5
        input_data = (np.float32(input_data) - input_mean) / input_std
        
    model.set_tensor(input_details[0]['index'], input_data)
    model.invoke()
    
    
    # Get Data
    boxes = model.get_tensor(output_details[0]['index'])[0] 
    scores = model.get_tensor(output_details[2]['index'])[0] 
    
    locations = []
    if( len(scores) == 0 ) : 
        return []
    for i in range(len(scores)):
        if ((scores[i] > threshold) and (scores[i] <= 1.0)):
            
            top = int(max(1,(boxes[i][0] * imgH)))
            left  = int(max(1,(boxes[i][1] * imgW)))
            bottom= int(min(imgH,(boxes[i][2] * imgH)))
            right = int(min(imgW,(boxes[i][3] * imgW)))

            locations.append( (left, top,right, bottom ) )
            
    return locations
    
    
def landmark(image, locations):         
    # Open Model
    face_recognition_model = face_recognition_models.face_recognition_model_location()
    face_encoder = dlib.face_recognition_model_v1(face_recognition_model)
        
    # Raw Landmark
    raw_landmarks = _raw_face_landmarks(image, locations)
    
    # Make data for train 
    return [np.array(face_encoder.compute_face_descriptor(image, raw_landmark_set, 1)) for raw_landmark_set in raw_landmarks]
    
def register(model_name, image, label) :
    cwd = os.getcwd()
    if model_name.find('.') > -1 :
        model_name = model_name.split('.')[0]
        
    label_path = os.path.join(cwd, model_name, label)
    try:
        if not os.path.exists(label_path):
            os.makedirs(label_path)
            print ('Success: Creating directory. ' +  label_path)
        else:
            print ('Success: Exist directory. ' +  label_path)

   except OSError:

              print ('Error: Creating directory. ' +  label_path)
    
    image_path = os.path.join(label_path, str(uuid.uuid4()).split('-')[0] + '.jpg')
    
    cv2.imwrite(image_path, image)
    
    
def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]

    
def registerList(model_name) :
    imageList = []
    
    cwd = os.getcwd()
    if model_name.find('.') > -1 :
        model_name = model_name.split('.')[0]    
    model_path =  os.path.join(cwd, model_name)

    if os.path.isdir(model_path) == False :
        return imageList
    
    for class_dir in os.listdir(model_path):
        if not os.path.isdir(os.path.join(model_path, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(model_path, class_dir)):
            imageList.append(img_path)
    
    return imageList
    
    
def train_face(model_name, knn_algo='ball_tree') :

    image_dir = model_name
    if model_name.find('.') > -1 :
        image_dir = model_name.split('.')[0]    
    else :
        model_name = model_name +'.clf'
        
    cwd = os.getcwd()
    image_path =  os.path.join(cwd, image_dir)
    model_save_path =  os.path.join(cwd, model_name)
    
    if os.path.isdir(image_path) == False :
        return None
        
    images = []
    X = []
    y = []
    
    n_neighbors = len(os.listdir(image_path))
    
    # Loop through each person in the training set
    for class_dir in os.listdir(image_path):
        if not os.path.isdir(os.path.join(image_path, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(image_path, class_dir)):
            image = load_image(img_path)

            face_bounding_boxes = face_locations(image)
            left = face_bounding_boxes[0][0]
            top = face_bounding_boxes[0][1]
            right = face_bounding_boxes[0][2]
            bottom = face_bounding_boxes[0][3]
            
            images.append(image[top:bottom, left:right])
            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the training set
                known_face = landmark(image, face_bounding_boxes)[0]
                X.append(known_face)
                y.append(class_dir)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance', )
    knn_clf.fit(X, y)
    
        # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf


    
def predict_faces(model_name, image, locations, threshold=0.8) :      
    if len(locations) == 0:
        return []
        
    image_dir = model_name
    if model_name.find('.') > -1 :
        image_dir = model_name.split('.')[0]    
    else :
        model_name = model_name +'.clf'
        
    cwd = os.getcwd()
    image_path =  os.path.join(cwd, image_dir)
    n_neighbors = len(os.listdir(image_path))
    
    faces_encodings = landmark(image, locations)
    
    knn_clf = load_knn(model_name)
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=n_neighbors)
    are_matches = [closest_distances[0][i][0] <= threshold for i in range(len(locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), locations, are_matches)]
    
    
    
def show_prediction(image, predictions, is_showing=False) :

    #frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    for name, (left, top, right, bottom) in predictions:
        cv2.rectangle(image, (left,top), (right,bottom), (10, 255, 0), 4)
            
        # Draw label
        #object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
        label = name
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
        label_top = max(top, labelSize[1] + 10) # Make sure not to draw label too close to top of window
        cv2.rectangle(image, (left, label_top-labelSize[1]-10), (left+labelSize[0], label_top+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
        cv2.putText(image, label, (left, label_top-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
        
        
    return image
    
    
def super_resolution(image) :
    # Location of model weights (needed for demo)
    weights_file = utils.get_mode_path()

    gan_generator = generator()
    gan_generator.load_weights(weights_file)

    gan_sr = resolve_single(gan_generator, image)
    gan_sr = resolve_single(gan_generator, gan_sr)
    return np.array(gan_sr)
    
    
    