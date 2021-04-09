import cv2
import time
from .. import config
from . import ai
class Camera():
    def __init__(self):
        self._ai=ai.Ai()

    #----摄像头抓拍识字
    def CameraCaptureOcr(self,image="CaptureOcr.png",e="low"):
        cap = cv2.VideoCapture( 0 )
        while (1):

            ret, frame = cap.read()
            cv2.imshow( "capture", frame )
            if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
                cv2.imwrite( str( config._words_path ) + image, frame )
                break
        cap.release()
        cv2.destroyAllWindows()

        # res=pystargate.image.WordsCapture(1,1,111,111,"1.bmp")
        # print(res)
        res = self._ai.Ocr( image,e )
        return res

    #----摄像头抓拍识图
    def CameraCaptureImage(self,image="CaptureImage.png"):
        cap = cv2.VideoCapture( 0 )
        while (1):

            ret, frame = cap.read()
            cv2.imshow( "capture", frame )
            if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
                cv2.imwrite( str( config._words_path ) + image, frame )
                break
        cap.release()
        cv2.destroyAllWindows()

        # res=pystargate.image.WordsCapture(1,1,111,111,"1.bmp")
        # print(res)
        res = self._ai.ImageSynthesis( image )
        return res

    #----摄像头抓拍
    def CameraCapture(self,image="Capture.png"):
        cap = cv2.VideoCapture( 0 )
        while (1):

            ret, frame = cap.read()
            cv2.imshow( "capture", frame )
            if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
                cv2.imwrite( str( config._image_path ) + image, frame )
                break
        cap.release()
        cv2.destroyAllWindows()

    #----摄像头连续抓拍，t为抓拍间隔时间
    def CameraCaptureGo(self,image="CaptureGo.png",t=2):
        cap = cv2.VideoCapture( 0 )
        while (1):
            ret, frame = cap.read()
            cv2.imshow( "capture", frame )
            time.sleep(t)
            cv2.imwrite( str( config._image_path ) + image, frame )
            if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
                break
        cap.release()
        cv2.destroyAllWindows()