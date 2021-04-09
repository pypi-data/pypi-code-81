import matplotlib.image as mpimg
import matplotlib.pyplot as plt

import cv2

def read(file_path):
  return mpimg.imread(file_path)

def save(file_path, img):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
  cv2.imwrite(file_path, img)

def show(img, grid=False, size=(12,12)):
  plt.figure(figsize=size)
  plt.grid(grid)
  plt.imshow(img)
  plt.show()

def rectangle(img, lt, rb, thickness=3):
  return cv2.rectangle(img, lt, rb, (255, 0, 0), thickness=thickness)

def line(img, pt1, pt2, thickness=3):
  return cv2.line(img, pt1, pt2, (255, 0, 0), thickness=thickness)

def circle(img, center, axes, thickness=3):
  return cv2.circle(img, center, radius, (255, 0, 0), thickness=thickness)

