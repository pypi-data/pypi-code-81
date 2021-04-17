# -*- coding: utf-8 -*-

# @File  : camera_read.py
# @Author: Andy.yang
# @Date  : 2021/02/22
# @Software: VS Code

import time
import threading
from os.path import dirname, realpath, join

import cv2


class Camera:
    def __init__(self, id_camera=0, num_of_all_cameras=5):
        """
        define the Camera class to operate camera(logitech)

        id_camera: the index of logitech in OS(it should be 0 or 1). 0 means it's the only camera, and
                   1 means there is another camera in laptop-PC
        num_of_all_cameras: this value is used for iterated to calcated the camera's number of PC.
        """
        self.id_camera = id_camera
        self.num_cam = num_of_all_cameras

        self._setDefaultParams()

    def _setDefaultParams(self):
        self.num_cam_store_count = 0
        self.st_open_cam = False
        self.st_close_cam = False
        self.st_write_video = False

        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')

        self.cap = cv2.VideoCapture(self.id_camera, cv2.CAP_DSHOW)
        self.pho_width = self.cap.get(3)
        self.pho_height = self.cap.get(4)
        # self.pho_fps = self.cap.get(5)
        self.pho_fps = 25

    def _setVideoStorePath(self, store_path):
        self.outfile = cv2.VideoWriter(store_path, self.fourcc, int(self.pho_fps),
                                       (int(self.pho_width), int(self.pho_height)))

    def setWriteVideo(self, status):
        if not self.st_write_video:
            DIR_PATH = dirname(dirname(realpath(__file__)))
            cur_time = time.strftime("%Y-%m-%d %H hour %M min %S sec",
                                     time.localtime(time.time()))
            data_store_path = join(DIR_PATH, "data", f"{cur_time}_{self.num_cam_store_count}.avi")
            self.num_cam_store_count +=1
            self._setVideoStorePath(data_store_path)
        self.st_write_video = status

    def openCamera(self):
        """
        This function will open the camera.
        """

        while (1):
            if self.st_close_cam:
                self.st_close_cam = False
                break
            else:
                ret, frame = self.cap.read()
                if ret:
                    self.st_open_cam = True
                    if self.st_write_video:
                        self.outfile.write(frame)
                    else:
                        pass
                    cv2.imshow("capture", frame)
                    key = cv2.waitKey(1)
                    if key == ord('q'):
                        self.closeCamera()
                        break
                else:
                    print("Open Camera Error!")

    def closeCamera(self):
        """
        This function will close the camera.
        """
        if self.st_open_cam:
            self.st_close_cam = True
            self.st_open_cam = False
            self.cap.release()
            cv2.destroyAllWindows()

    def getCameraNum(self):
        cnt = 0
        for device in range(0, self.num_cam):
            stream = cv2.VideoCapture(device, cv2.CAP_DSHOW)

            grabbed = stream.grab()
            stream.release()
            if not grabbed:
                break
            else:
                cnt += 1

        return cnt

    def setCameraID(self, id_cam):
        self.id_camera = id_cam
