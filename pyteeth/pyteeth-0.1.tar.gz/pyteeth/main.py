import glob
import os

import cv2 

from detector import ObjectDetector

class Teeth():
    def __init__(self):
        pass
    def detect_top_six_teeth_for_edit(self , image):
        detector = ObjectDetector(loadPath="teeth_detector.svm")
        x,y,xb,yb = detector.detect(image)
        print(x,y,xb,yb)
        cv2.rectangle(image,(x,y),(xb,yb),(0,0,255),2)
        cv2.putText(image,"top6_teeth",(x+5,y-5),cv2.FONT_HERSHEY_SIMPLEX,1.0,(128,255,0),2)
        cv2.imshow("Detected",image)
        cv2.waitKey(0)

    def detect_each_tooth_for_edit(self , image , coords):
        x , y , xb , yb = coords
        w = xb-x
        h = yb-y
        w_step = w // 6
        print(w_step , x,y,xb,yb ,w)
        for x_line in range(x  , xb , w_step):
            cv2.line(image, (x_line, y), (x_line, yb), (0, 255, 0), thickness=2)
        cv2.imshow("Detected",image)
        cv2.waitKey(0)

def main():
    images = os.listdir("test_images/")
    for image in images:
        teeth = Teeth()
        img = cv2.imread(f"./test_images/{image}")
        teeth.detect_top_six_teeth_for_edit(img)
        teeth.detect_each_tooth_for_edit(img,[155,162,447,275])

if __name__ == "__main__":
    main()