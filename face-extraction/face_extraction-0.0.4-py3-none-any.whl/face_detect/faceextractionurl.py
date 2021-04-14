import cv2
import io
import PIL
import numpy as np
import requests
import logging



#Return Face
def __returnFaces(image):
    """

    :param image:doc from which face to be extracted
    :return:array of faces extracted
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(20,20)
        )
    return faces;

#Rotate image
def __rotate_image(image):
    """

    :param image: Image that to be rotated
    :return: rotated Image, alligned at 0 degree
    """
    rotatedImage = image
    for i in range(4):
        faces =  __returnFaces(rotatedImage)
        if not len(faces)> 0:
            img_rotate_90_clockwise = cv2.rotate(rotatedImage, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite('rotated_image.jpg', img_rotate_90_clockwise)
            rotatedImage = img_rotate_90_clockwise
    return rotatedImage;

#extract face for the given doc url
def getFace(url):
    """

    :param url: Url for the image
    :return: numpy array image object
    """
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    img = PIL.Image.open(image_bytes)
    imagePath = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    image = __rotate_image(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(20,20)
    )
    logging.info("Found {0} Faces.".format(len(faces)))
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = image[y:y + h, x:x + w]
        logging.info("Object found. Saving locally.")
        cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)
        status = cv2.imwrite('faces_detected.jpg', image)
        logging.info("Image faces_detected.jpg written to filesystem: ", status)
    return roi_color



