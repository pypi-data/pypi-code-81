from paddleclas import PaddleClas
import cv2
clas = PaddleClas(model_name='ResNet50', use_gpu=True, use_tensorrt=False, top_k=5, is_preprocessed=False)
image_file='docs/images/whl/demo.jpg'
result=clas.predict(image_file)
print(result)


print("***********")
clas = PaddleClas(model_name='ResNet50', use_gpu=True, use_tensorrt=False, top_k=5)
img = cv2.imread(image_file)
res = clas.predict(img)
print(res)

print("***********")
clas = PaddleClas(model_name='ResNet50', use_gpu=True, use_tensorrt=False, top_k=5, is_preprocessed=True)
img = cv2.imread(image_file)[:, :, ::-1]
import argparse
from tools.infer.utils import preprocess
args = argparse.Namespace(resize_short=256, resize=224, normalize=True)
img = preprocess(img, args)
res = clas.predict(img)
print(res)
