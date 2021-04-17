import cv2
import time
from .. import config
from . import ai
class Camera():
    def __init__(self):
        self._ai=ai.Ai()


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