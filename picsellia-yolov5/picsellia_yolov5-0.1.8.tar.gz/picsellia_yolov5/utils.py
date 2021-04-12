import os
from PIL import Image
import tqdm
import shutil 
import yaml
from ruamel.yaml import YAML
from pathlib import Path
import re
import torch
from numpy import random

from yolov5.models.experimental import attempt_load
from yolov5.utils.datasets import LoadStreams, LoadImages
from yolov5.utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from yolov5.utils.plots import plot_one_box
from yolov5.utils.torch_utils import select_device, load_classifier, time_synchronized

def to_yolo(pxl_annotations_dict=None,labelmap=None, base_imgdir=None, targetdir=None, prop=0.7, copy_image=True):
    """
        Simple utility function to transcribe a Picsellia Format Dataset into YOLOvX
    """

    # Creating tree directory for YOLO
    if not os.path.isdir(targetdir):
        os.mkdir(targetdir)

    for dirname in ["images", "labels"]:
        if not os.path.isdir(os.path.join(targetdir, dirname)):
            os.mkdir(os.path.join(targetdir, dirname))

    for path in os.listdir(targetdir):
        for step in ['train', 'val']:
            if not os.path.isdir(os.path.join(targetdir, path, step)):
                os.mkdir(os.path.join(targetdir, path, step))
  
    train_prop = int(len(os.listdir(base_imgdir)))*prop

    trainset = {}
    testset = {}

    categories = list(labelmap.values()) 
    trainrep = [0 for e in categories]
    train_ids = []
    testrep = [0 for e in categories]
    test_ids = []

    for i, path in tqdm.tqdm(enumerate(os.listdir(base_imgdir))):
        if i < train_prop:
            step = "train"
        else:
            step = "val"
        
        img_id = path 
        img = Image.open(os.path.join(base_imgdir, img_id))

        width, height = img.size
        success, objs = find_matching_annotations(pxl_annotations_dict, img_id)
        

        if copy_image:
            img.save(os.path.join(targetdir,"images", step, os.path.splitext(img_id)[0] + '.png', ), 'PNG')
        else:
            shutil.move(os.path.join(base_imgdir, img_id), os.path.join(targetdir, 'images', step, img_id))

        if success:
            if step == "train":
                train_ids.append(objs["internal_picture_id"])
            else:
                test_ids.append(objs["internal_picture_id"])
            label_name = "{}.txt".format(os.path.splitext(img_id)[0])
            with open(os.path.join(targetdir,'labels',step, label_name), 'w') as f:
                for a in objs["annotations"]:
                    x1 = a["rectangle"]["left"]
                    y1 = a["rectangle"]["top"]
                    w = a["rectangle"]["width"]
                    h = a["rectangle"]["height"]
                    for k,v in labelmap.items():
                        if v == a["label"]:
                            category_idx =  int(k) -1

                    if step == "train":
                        trainrep[categories.index(a["label"])] += 1 
                        
                    else:
                        testrep[categories.index(a["label"])] += 1 

                    f.write(f"{category_idx} {(x1 + w / 2)/width} {(y1 + h / 2)/height} {w/width} {h/height}\n")  

            train_rep = {
                "categories": categories,
                "train_repartition": trainrep,
                "image_list": train_ids
            }

            test_rep = {
                "categories": categories,
                "train_repartition": testrep,
                "image_list": test_ids
            }

            
        else:
            continue
    return train_rep, test_rep
        
def find_matching_annotations(dict_annotations=None, imgpath=None):
    for ann in dict_annotations["annotations"]:
        if imgpath.split('/')[-1] == ann["external_picture_url"]:
            return True, ann 
    return False, None


def generate_yaml(yamlname, targetdir, labelmap):
    print("Data yaml updated")
    if not os.path.isdir(os.path.join(targetdir, "data")):
        os.mkdir(os.path.join(targetdir, "data"))

    dict_file = {   
                    'train' : '{}/{}/train'.format(targetdir, "images"),
                    'val' : '{}/{}/val'.format(targetdir, "images"),
                    'nc': len(labelmap),
                    'names': list(labelmap.values())
                    }
                
    with open('{}/data/{}.yaml'.format(targetdir, yamlname), 'w') as file:
        documents = yaml.dump(dict_file, file)
    return  

def edit_model_yaml(label_map, experiment_name, config_path=None):


    for path in os.listdir(config_path):
        if path.endswith('yaml'):
            ymlpath = os.path.join(config_path, path)


    path = Path(ymlpath)



    with open(ymlpath, 'r') as f:
        data = f.readlines()

    temp = re.findall(r'\d+', data[1]) 
    res = list(map(int, temp)) 

    data[1] = data[1].replace(str(res[0]), str(len(label_map)))

    if config_path is None:
        opath = '.'+ymlpath.split('.')[1]+experiment_name+'.'+ymlpath.split('.')[2]
    else:
        opath = './'+ymlpath.split('.')[0]+experiment_name+'.'+ymlpath.split('.')[1]
    with open(opath, "w") as f:
        for line in data:
            f.write(line)

    if config_path is None:
        tmp = opath.replace('./yolov5','.')
    
    else:
        tmp = ymlpath.split('.')[0]+experiment_name+'.'+ymlpath.split('.')[1]

    return tmp

def tf_events_to_dict(path, type=''):
    '''Get a dictionnary of scalars from the tfevent inside the training directory.

        Args: 
            path: The path to the directory where a tfevent file is saved or the path to the file.
        
        Returns:
            A dictionnary of scalars logs.
    '''
    log_dict = {}
    if path.startswith('events.out'):
        if not os.path.isfile(path):
            raise FileNotFoundError('No tfEvent file found at {}'.format(path)) 
    else:
        if os.path.isdir(path):
            files = os.listdir(path)
            file_found = False
            for f in files:
                if not file_found:
                    if f.startswith('events.out'):
                        path = os.path.join(path,f)
                        file_found = True 
    if not file_found:
        raise FileNotFoundError('No tfEvent file found in this directory {}'.format(path))
    for summary in summary_iterator(path):
        for v in summary.summary.value:
            if not 'image' in v.tag:
                key = '-'.join(v.tag.split('/'))
                if v.tag in log_dict.keys():
                    decoded = tf.compat.v1.decode_raw(v.tensor.tensor_content, tf.float32)
                    log_dict[v.tag]["steps"].append(str(len(log_dict[v.tag]["steps"])+1))
                    log_dict[v.tag]["values"].append(str(tf.cast(decoded, tf.float32).numpy()[0]))
                else:
                    decoded = tf.compat.v1.decode_raw(v.tensor.tensor_content, tf.float32)
                    if type=='train':
                        scalar_dict = {"steps": [0], "values": [str(tf.cast(decoded, tf.float32).numpy()[0])]}
                        log_dict[v.tag] = scalar_dict
                    if type=='eval':
                        log_dict[v.tag] = str(tf.cast(decoded, tf.float32).numpy()[0])

    return log_dict

def detect(weights, path, thresh=0.7, size=640, iou_thresh=0.45, augment=True, agnostic_nms=True):
    source, imgsz = path, size
    # Initialize
    set_logging()
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    half = device != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    save_img = True
    dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    predictions = []
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=augment)[0]
        print(type(pred))
        # Apply NMS
        pred = non_max_suppression(pred, thresh, iou_thresh, agnostic=agnostic_nms)
        t2 = time_synchronized()
        print(type(pred))
        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)
        predictions.append(pred[0].cpu().numpy())
        print(type(predictions))
        # Process detections
        for i, det in enumerate(pred):  # detections per image
            p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string


            # Print time (inference + NMS)
            print(f'{s}Done. ({t2 - t1:.3f}s)')
    return predictions

def setup_hyp(exp_name, cfg, checkpoint_dir, params={}, label_map=[]):
    YOLOSIZE = cfg.split('/')[2][6]
    YOLODIR = 'YOLO-{}'.format(exp_name)

    model_exp_name = "yolov5{}_{}".format(YOLOSIZE, exp_name)
    data_yaml = '{}/data/{}.yaml'.format(YOLODIR, exp_name)

    tmp = os.listdir(checkpoint_dir)
    for f in tmp:
        if f.endswith('.pt'):
            weight_path = os.path.join(checkpoint_dir, f)
        if f.endswith('.yaml'):
            hyp_path = os.path.join(checkpoint_dir, f)
    

    opt = Opt()
    opt.batch_size = 4 if not 'batch_size' in params.keys() else params["batch_size"]
    opt.epochs = 100 if not 'steps' in params.keys() else params["steps"] 
    opt.data = data_yaml
    opt.cfg = cfg 
    opt.weights = weight_path 
    opt.name = model_exp_name
    opt.img_size =  [640, 640] if not 'input_shape' in params.keys() else params["input_shape"]
    opt.hyp = hyp_path if not 'hyperparams' in params.keys() else params["hyperparams"]

    opt.resume = False
    opt.bucket = ''
    opt.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    opt.local_rank = -1 
    opt.log_imgs = 4
    opt.workers = 4
    opt.project = '{}/runs/train'.format(YOLODIR)
    opt.entity = None 
    opt.evolve = False
    opt.exist_ok = True
    opt.single_cls = (len(label_map) == 1)
    opt.adam = True
    opt.linear_lr = True
    opt.sync_bn = False
    opt.cache_images = False 
    opt.multi_scale = True
    opt.rect = True
    opt.image_weights = False
    opt.quad = False
    opt.noautoanchor = False
    opt.notest = False
    opt.nosave = False
    with open(opt.hyp) as f:
        hyp = yaml.load(f, Loader=yaml.SafeLoader)  # load hyps

    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    return hyp, opt, device

def find_final_run(YOLODIR, exp_name):
    runs_path = os.path.join(YOLODIR, 'runs', 'train')
    dirs = os.listdir(runs_path)
    if len(dirs) == 1:
        return os.path.join(runs_path, dirs[0])
    base = dirs[0][:7]
    lower_exp_name = exp_name.replace('-', '_')
    name = base + '_' + lower_exp_name
    truncate_dirs = [int(n[len(name)-1:]) for n in dirs]
    last_run_nb = max(truncate_dirs)
    return os.path.join(runs_path, name + str(last_run_nb))

def get_batch_mosaics(final_run_path):
    test_batch0_labels = None
    test_batch0_pred = None
    test_batch1_labels = None
    test_batch1_pred = None
    test_batch2_labels = None
    test_batch2_pred = None
    if os.path.isfile(os.path.join(final_run_path, 'test_batch0_labels.jpg')):
        test_batch0_labels = os.path.join(final_run_path, 'test_batch0_labels.jpg')
    if os.path.isfile(os.path.join(final_run_path, 'test_batch0_pred.jpg')):
        test_batch0_pred = os.path.join(final_run_path, 'test_batch0_pred.jpg')
    if os.path.isfile(os.path.join(final_run_path, 'test_batch1_labels.jpg')):
        test_batch1_labels = os.path.join(final_run_path, 'test_batch1_labels.jpg')
    if os.path.isfile(os.path.join(final_run_path, 'test_batch1_pred.jpg')):
        test_batch1_pred = os.path.join(final_run_path, 'test_batch1_pred.jpg')
    if os.path.isfile(os.path.join(final_run_path, 'test_batch2_labels.jpg')):
        test_batch2_labels = os.path.join(final_run_path, 'test_batch2_labels.jpg')
    if os.path.isfile(os.path.join(final_run_path, 'test_batch2_pred.jpg')):
        test_batch2_pred = os.path.join(final_run_path, 'test_batch2_pred.jpg')
    return test_batch0_labels, test_batch0_pred, test_batch1_labels, test_batch1_pred, test_batch2_labels, test_batch2_pred

def get_weights_and_config(final_run_path):
    last_weights = None
    best_weights = None
    hyp_yaml = None
    if os.path.isfile(os.path.join(final_run_path, 'weights', 'best.pt')):
        best_weights = os.path.join(final_run_path, 'weights', 'best.pt')
    if os.path.isfile(os.path.join(final_run_path, 'weights', 'last.pt')):
        last_weights = os.path.join(final_run_path, 'weights', 'last.pt')
    if os.path.isfile(os.path.join(final_run_path, 'hyp.yaml')):
        hyp_yaml = os.path.join(final_run_path, 'hyp.yaml')
    return best_weights, last_weights, hyp_yaml

def get_metrics_curves(final_run_path):
    confusion_matrix = None
    F1_curve = None
    labels_correlogram = None
    P_curve = None
    PR_curve = None
    R_curve = None
    if os.path.isfile(os.path.join(final_run_path, 'confusion_matrix.png')):
        confusion_matrix = os.path.join(final_run_path, 'confusion_matrix.png')
    if os.path.isfile(os.path.join(final_run_path, 'F1_curve.png')):
        F1_curve = os.path.join(final_run_path, 'F1_curve.png')
    if os.path.isfile(os.path.join(final_run_path, 'labels_correlogram.jpg')):
        labels_correlogram = os.path.join(final_run_path, 'labels_correlogram.jpg')
    if os.path.isfile(os.path.join(final_run_path, 'P_curve.png')):
        P_curve = os.path.join(final_run_path, 'P_curve.png')
    if os.path.isfile(os.path.join(final_run_path, 'PR_curve.png')):
        PR_curve = os.path.join(final_run_path, 'PR_curve.png')
    if os.path.isfile(os.path.join(final_run_path, 'R_curve.png')):
        R_curve = os.path.join(final_run_path, 'R_curve.png')
    return confusion_matrix, F1_curve, labels_correlogram, P_curve, PR_curve, R_curve

def send_run_to_picsellia(experiment, YOLODIR):
    final_run_path = find_final_run(YOLODIR, experiment.experiment_name)
    best_weigths, last_weights, hyp_yaml = get_weights_and_config(final_run_path)

    if best_weigths is not None:
        experiment.store('best-weights', best_weigths)
    if last_weights is not None:
        experiment.store('last-weights', last_weights)
    if hyp_yaml is not None:
        experiment.store('checkpoint-data-latest', hyp_yaml)
    for curve in get_metrics_curves(final_run_path):
        if curve is not None:
            name = curve.split('/')[-1].split('.')[0]
            experiment.log(name, curve, 'image')
    for batch in get_batch_mosaics(final_run_path):
        if batch is not None:
            name = batch.split('/')[-1].split('.')[0]
            experiment.log(name, batch, 'image')


class Opt():
    pass