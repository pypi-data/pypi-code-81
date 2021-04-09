from .libs import camera
_camera=camera.Camera()

def CaptureOcr(image="CaptureOcr.png",e="low"):
    return _camera.CameraCaptureOcr(image,e)

def CaptureImage(image="CaptureImage.png"):
    return _camera.CameraCaptureImage(image)

def Capture(image="Capture.png"):
    return _camera.CameraCapture(image)

def CaptureGo(image="CaptureGo.png",t=2):
    return _camera.CameraCaptureGo(image,t)