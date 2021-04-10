from .networks import RecognitionModel
import torch
from torchvision import transforms
import cv2 as cv
import numpy as np
import os
from facenet_pytorch import MTCNN


class MaskRecognition(object):
    def __init__(self, device=0):
        self.device = torch.device(f"cuda:{device}") if device >= 0 else torch.device("cpu")
        self.model = RecognitionModel().to(self.device)
        self.model.load_state_dict(torch.load(os.path.join(os.path.dirname(__file__), "model", "model.pth"), map_location=self.device))
        self.mtcnn = MTCNN(keep_all=True, device=self.device)
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5]*3, std=[0.5]*3)
        ])
        self.result = {0: "with_mask", 1: "without_mask"}

    def _predict(self, image):
        tensor = self.transform(image).unsqueeze(0).to(self.device)
        probability = torch.exp(self.model(tensor)[0])
        prediction = torch.argmax(probability).item()
        return self.result[prediction], probability[prediction].item() * 100

    def recognize(self, frame, color="rgb"):
        frame = np.array(frame)
        boxes, _ = self.mtcnn.detect(frame)
        rois = []
        if boxes is not None:
            for i in range(len(boxes)):
                x1, y1, x2, y2 = int(round(boxes[i][0])), int(round(boxes[i][1])), int(round(boxes[i][2])), int(round(boxes[i][3]))
                x1, y1, x2, y2 = max(x1, 0), max(y1, 0), max(x2, 0), max(y2, 0)
                rois.append([frame[y1:y2, x1:x2, :], [x1, y1, x2, y2]])
            for n, roi in enumerate(rois):
                prediction, percent = self._predict(roi[0])
                x1, y1, x2, y2 = roi[1]
                box_color = [255, 0, 0] if prediction == "without_mask" else [0, 255, 0]
                d = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                if percent > 10 and d > 100:
                    cv.rectangle(frame, (x1, y1), (x2, y2), box_color, 1)
                    cv.rectangle(frame, (x1, y1 - 15), (x1 + (x2 - x1), y1), box_color, -1)
                    cv.putText(frame, prediction + f" {percent:.2f}%", (x1, y1), cv.FONT_HERSHEY_PLAIN, 1, [0, 0, 0], 1)
        else:
            pass
        if color == "bgr":
            return cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        else:
            return frame

    def cam_capture(self, device_id=0):
        cam = cv.VideoCapture(device_id)
        success, frame = cam.read()
        while success:
            success, frame = cam.read()
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            predicted_frame = self.recognize(np.flip(frame, 1), "bgr")
            cv.imshow("image", predicted_frame)
            key = cv.waitKey(10)
            if key & 0xff == 27:
                break
