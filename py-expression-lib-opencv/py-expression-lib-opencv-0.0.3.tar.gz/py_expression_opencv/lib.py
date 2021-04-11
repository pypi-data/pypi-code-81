from py_expression.core import Exp
import cv2 as cv
import numpy as np  
from os import path,getcwd

def loadOpenCvExpressions(exp:Exp):
    cvtypes = {
        "uint8": cv.CV_8U,
        "uint16": cv.CV_16U,
        "int8": cv.CV_8S,
        "int16": cv.CV_16S,
        "float32": cv.CV_32F,
        "float64": cv.CV_64F
    }
    exp.addEnum('ColorConversion',{"BGR2GRAY":6,"BGR2HSV":40,"BGR2RGB":4,"GRAY2BGR":8
                                    ,"HSV2BGR":54,"HSV2RGB":55,"RGB2GRAY":7,"RGB2HSV":41})
    exp.addEnum('BorderTypes',{"CONSTANT":0,"REPLICATE":1,"REFLECT":2,"WRAP":3
                                ,"REFLECT_101":4,"TRANSPARENT":5,"DEFAULT":4,"ISOLATED":16})
    exp.addEnum('MorphTypes',{"ERODE":0,"DILATE":1,"OPEN":2,"CLOSE":3
                                ,"GRADIENT":4,"TOPHAT":5,"BLACKHAT":6,"HITMISS":7}) 
    exp.addEnum('MorphShapes',{"RECT":0,"CROSS":1,"ELLIPSE":3}) 
    exp.addEnum('RotateAngle',{"90":90,"180":180,"270":270}) 


    def cvCanny(image,threshold1,threshold2):
        color = False
        if len(image.shape) >= 3:
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            color = True
        output = cv.Canny(image,threshold1,threshold2)
        return cv.cvtColor(output, cv.COLOR_GRAY2BGR) if color else output
    def cvRotate(image,angle):
        image = np.copy(image)
        angle_rad = np.radians(angle)
        h, w = image.shape[:2]
        trans1 = np.array([[1, 0, -w / 2],
                            [0, 1, -h / 2],
                            [0, 0, 1]],
                            dtype=np.float32)
        if angle % 180 == 90:
            h, w = w, h
        trans2 = np.array([[1, 0, w / 2],
                            [0, 1, h / 2],
                            [0, 0, 1]],
                            dtype=np.float32)
        rot = np.array([[np.cos(angle_rad), -np.sin(angle_rad), 0],
                        [np.sin(angle_rad), np.cos(angle_rad), 0],
                        [0, 0, 1]],
                            dtype=np.float32)

        mat = np.dot(np.dot(trans2, rot), trans1)
        return cv.warpAffine(image, mat[:2], (w, h))
    def cvResize(image,percent):        
        width = int(image.shape[1] * percent / 100)
        height = int(image.shape[0] * percent / 100)
        dim = (width, height)
        return cv.resize(image, dim, interpolation = cv.INTER_AREA)

    # TODO: no funciona, revisar
    def cvCrop(image,rectangle:dict):        
        cw = int(image.shape[1] * rectangle['x'])
        w2 = rectangle['width'] // 2
        ch = int(image.shape[0] * rectangle['y'])
        h2 = rectangle['height'] // 2
        return image[max(0, ch - h2):ch + h2, max(0, cw - w2):cw + w2]
    def cvGaussianBlur3D(image,kernel,coordinate,borderType):        
        image = np.copy(image)
        for z in image:
            cv.GaussianBlur(z, (kernel, kernel), coordinate['x'], z, coordinate['y'], borderType)
        for y in range(image.shape[1]):
            xz = image[:, y]
            cv.GaussianBlur(xz, (1, kernel), 0, xz, coordinate['z'], borderType)
        return image
    def cvColorNormalizer(image,outmean=128,outstddev=64):
        mean, stddev = cv.meanStdDev(image)
        if stddev == 0: stddev = 1
        output = (image.astype(np.float32) - mean) * (outstddev/stddev) + outmean
        return np.clip(output, 0, 255).astype(image.dtype)
    def cvContrastChange(image,factor):
        avg = cv.mean(image)
        output = cv.add(cv.subtract(np.float64(image), avg) * factor, avg)
        return cv.add(np.zeros(output.shape, image.dtype), output, dtype=cvtypes[image.dtype.name])
    def cvMorphologyEx(image,operation,elementType,elementSize,iterations):
        image = np.copy(image)
        element = cv.getStructuringElement(elementType, (elementSize, elementSize))
        return cv.morphologyEx(image, operation, element, iterations=iterations,)
    def cvDilate(image,elementType,elementSize,iterations):
        image = np.copy(image)
        element = cv.getStructuringElement(elementType, (elementSize, elementSize))
        return cv.dilate(image, element, iterations=iterations)
    def cvErode(image,elementType,elementSize,iterations):
        image = np.copy(image)
        element = cv.getStructuringElement(elementType, (elementSize, elementSize))
        return cv.erode(image, element, iterations=iterations)  
    def cvAdd(image1,image2):
        output=None
        cv.add(image1, image2, output)        
        return output
    def cvAdds(images):
        output=None
        first= True
        for input in images:
            if first:
                output = input
                first=False
            else:
                cv.add(output, input, output)
        return output
    def cvVideoCapture(number=0):
        return cv.VideoCapture(number)
    def cvVideoRead(cam):
        return cam.read() if cam.isOpened() else None
    def cvVideoRelease(cam):
        cam.release()


    # Pendings AverageOperator,MaxOperator,MinOperator,InvertOperator,ScalarMultiplyOperator,ScalarAddOperator 


    exp.addFunction('cvImread',cv.imread)
    exp.addFunction('cvImwrite',cv.imwrite)
    exp.addFunction('cvtColor',cv.cvtColor)
    exp.addFunction('cvCanny',cvCanny)
    exp.addFunction('cvRotate',cvRotate)
    exp.addFunction('cvResize',cvResize)
    exp.addFunction('cvCrop',cvCrop)
    exp.addFunction('cvBlur',cv.blur)
    exp.addFunction('cvGaussianBlur',cv.GaussianBlur)
    exp.addFunction('cvGaussianBlur3D',cvGaussianBlur3D)
    exp.addFunction('cvInRange',cv.inRange)
    exp.addFunction('cvColorNormalizer',cvColorNormalizer)
    exp.addFunction('cvContrastChange',cvContrastChange)
    exp.addFunction('cvMorphologyEx',cvMorphologyEx)
    exp.addFunction('cvDilate',cvDilate)
    exp.addFunction('cvErode',cvErode)
    exp.addFunction('cvAdd',cvAdd)
    exp.addFunction('cvAdds',cvAdds)
    exp.addFunction('cvSubtract',cv.subtract)
    exp.addFunction('cvAbsdiff',cv.absdiff)
    exp.addFunction('cvVideoCapture',cvVideoCapture)
    exp.addFunction('cvVideoRead',cvVideoRead)
    exp.addFunction('cvVideoRelease',cvVideoRelease)

    class Volume():
        def __init__(self,_path):        
            self._root = _path if path.isabs(_path) else path.join(getcwd(),_path) 
        def fullpath(self,_path):
            return path.join(self._root,_path)
    def createVolume(_path):return Volume(_path)

    exp.addFunction('Volume',createVolume)
    exp.addFunction('pathRoot',getcwd)
    exp.addFunction('pathJoin',path.join)

    exp.refresh()
