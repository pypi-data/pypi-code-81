from orientation_recognition.utils.tools import download_url
from fastai.metrics import error_rate  # 1 - accuracy
from fastai.vision import learner, models
from fastai.vision.data import ImageDataBunch, imagenet_stats
from fastai.vision.image import Image as fastaiImage
from fastai.vision.image import open_image, pil2tensor
from fastai.vision.learner import cnn_learner
from pathlib import Path
import numpy as np 

class Resnet34: 
    def __init__(self,config) -> None:
        img_size = config["face_orientation"]["img_size"]
        num_workers = config["face_orientation"]["num_workers"]
        no_check = config["face_orientation"]["no_check"]
        data_path = config["face_orientation"]["data_path"]
        model_name = "best_resnet34"
        path = Path(data_path)
        data = ImageDataBunch.from_folder(path, size=img_size, num_workers=num_workers, no_check=no_check).normalize(imagenet_stats)
        self.model = cnn_learner(data, models.resnet34, metrics=error_rate)
        self.model.load(model_name)

    def preprocess(self,pil_image,img_path:str = ""):
        if len(img_path) != 0: 
            return open_image(img_path)

        tensor = pil2tensor(pil_image,np.float32)
        tensor.div_(255)
        return fastaiImage(tensor)
    
    def predict(self,pil_img=None,img_path:str = ""):
        """ Model prediction
        If you don't specify the pil_img, then use the img_path directly
        
        Args:
            pil_img ([type], optional): Image.open('image_path').convert('RBG'). pil is PIL image at RGB mode
            img_path (str, optional): path of image

        Returns:
            parsed_pred (str): "0","90","180","270"
        """
        img = self.preprocess(pil_img, img_path)
        prediction = self.model.predict(img)
        parsed_pred = str(prediction[0])
        return parsed_pred
