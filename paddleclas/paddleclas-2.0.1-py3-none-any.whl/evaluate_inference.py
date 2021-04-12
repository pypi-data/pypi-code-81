import os
import numpy as np
import cv2
import paddle
from paddle.inference import Config
from paddle.inference import create_predictor
 
 
class Args():
    pass
 
 
def normalize_op(img):
    scale = np.float32(1.0 / 255.0)
    mean = np.array([0.485, 0.456, 0.406]).reshape((1, 1, 3)).astype('float32')
    std = np.array([0.229, 0.224, 0.225]).reshape((1, 1, 3)).astype('float32')
     
    return (img.astype('float32') * scale - mean) / std
 
 
def crop_op(img):
    w, h = (224, 224)
    img_h, img_w = img.shape[:2]
    w_start = (img_w - w) // 2
    h_start = (img_h - h) // 2
 
    w_end = w_start + w
    h_end = h_start + h
    return img[h_start:h_end, w_start:w_end, :]
 
 
def resize_op(img):
    img_h, img_w = img.shape[:2]
    percent = float(256) / min(img_w, img_h)
    w = int(round(img_w * percent))
    h = int(round(img_h * percent))
    return cv2.resize(img, (w, h))
 
 
def preprocess(img):
    img = resize_op(img)
    img = crop_op(img)
    img = normalize_op(img)
    img = img.transpose((2, 0, 1))
    return img
 
 
def postprocess(output):
    output = output.flatten()
    classes = np.argpartition(output, -5)[-5:]
    classes = classes[np.argsort(-output[classes])]
    scores = output[classes]
    return classes, scores
 
 
def predict(img, predictor):
    input_names = predictor.get_input_names()
    input_tensor = predictor.get_input_handle(input_names[0])
 
    output_names = predictor.get_output_names()
    output_tensor = predictor.get_output_handle(output_names[0])
 
    test_num = 500
    test_time = 0.0
 
    inputs = preprocess(img)
    inputs = np.expand_dims(inputs, axis=0).repeat(1, axis=0).copy()
    input_tensor.copy_from_cpu(inputs)
 
    predictor.run()
 
    output = output_tensor.copy_to_cpu()
    classes, scores = postprocess(output)
 
    return classes, scores
 
 
def set_config(args):
    config = Config(args.model_file, args.params_file)
    if args.use_gpu:
        config.enable_use_gpu(args.gpu_mem, 0)
    else:
        config.disable_gpu()
    config.disable_glog_info()
    config.enable_memory_optim()
    config.switch_use_feed_fetch_ops(False)
    config.switch_specify_input_names(True)
    return config
 
     
def main(args):
    config = set_config(args)
    predictor = create_predictor(config)
     
    image_list = []
    with open(args.val_file, 'r') as f:
        for line in f:
            image_path, label = line.strip('\n').split(' ')
            image_list.append((image_path, label))
    num = 0
    cor_num = 0
    for image_path, label in image_list:
        try:
            img = cv2.imread(os.path.join(args.val_dir, image_path))[:, :, ::-1]
            assert img is not None, "Error in loading image"
        except Exception as e:
            continue
        num += 1
        classes, scores = predict(img, predictor)
        print(classes, scores)
        if str(classes[0]) == label:
            cor_num += 1
    print("Total: {}, Correct: {}, Acc: {}".format(num, cor_num, cor_num/num))
 
 
if __name__ == "__main__":
    args = Args()
    args.use_gpu = True
    args.gpu_mem = 8000
    args.model_file = "./inference_models/best_model_xpu_resnet50_vd_infer/inference.pdmodel"
    args.params_file = "./inference_models/best_model_xpu_resnet50_vd_infer/inference.pdiparams"
    args.val_file = "/paddle/data/flowers102/val_list.txt"
    args.val_dir = "/paddle/data/flowers102/"
    main(args)
