import torchvision.ops
import torch
from collections import Counter
import numpy as np
import pandas as pd

def nms_reduction(predictions, thresh=0.05):
    #returns predictions after NMS
    fixed_indices = torchvision.ops.nms(predictions['boxes'], predictions['scores'], thresh)
    reduced_predictions = {'boxes': predictions['boxes'][fixed_indices], 'labels': predictions['labels'][fixed_indices],
                           'scores': predictions['scores'][fixed_indices]}
    return reduced_predictions


def get_objects_of_type(predictions, object_class, inc_scores=True):
    # extracts predictions for the class we wish to evaluate
    labels = predictions['labels']
    obj_ids = (labels == object_class).nonzero()
    if inc_scores == True:
        reduced_predictions = {'boxes': predictions['boxes'][obj_ids], 'labels': predictions['labels'][obj_ids],
                               'scores': predictions['scores'][obj_ids]}
    else:
        reduced_predictions = {'boxes': predictions['boxes'][obj_ids], 'labels': predictions['labels'][obj_ids]}
    return reduced_predictions


class EvoDAttack:
    def __init__(self, model, attack_class, iterations=25,
                 init_pop_size=4, thresh=0.05, max_val=0.1,
                 init_pop_mean=0, init_pop_dev=0.05, num_offspring=2,
                 mutation=True, mut_mean=0, mut_deviation=0.005, device='cuda', **kwargs):
        self.model = model
        self.attack_class = attack_class
        self.init_pop_size = init_pop_size
        self.thresh = thresh
        self.max_val = max_val
        self.iterations = iterations
        self.init_pop_mean = init_pop_mean
        self.init_pop_dev = init_pop_dev
        self.num_offspring = num_offspring
        self.mutation = mutation  # remove arg
        self.mut_mean = mut_mean
        self.mut_deviation = mut_deviation
        self.device = device
        self.pop_reduction = None

    def get_weakest(self, predictions):
        # takes in the predictions for the class we care about, and finds the weakest one
        scores = predictions['scores']
        weak_id = torch.argmin(scores)
        reduced_predictions = {'boxes': predictions['boxes'][weak_id], 'labels': predictions['labels'][weak_id],
                               'scores': predictions['scores'][weak_id]}
        return reduced_predictions

    def get_ground_truth(self, annots, wl_pred):
        ious = torchvision.ops.box_iou(wl_pred['boxes'], annots['boxes'].squeeze(dim=1))
        gt_idx = torch.argmax(ious, dim=1)[0]
        true_gt = {'boxes': annots['boxes'][gt_idx], 'labels': annots['labels'][gt_idx]}
        return true_gt

    def find_vulnerable(self, predicts, targ, thresh=0.05):
        # Finds the most vulnerable ground truth object of the class we wish to attack.
        obj_id = self.attack_class
        with torch.no_grad():
            red_preds = nms_reduction(predicts, thresh=thresh)
            object_preds = get_objects_of_type(predicts, obj_id, inc_scores=True)
            object_target = get_objects_of_type(targ, obj_id, inc_scores=False)
            if object_target['boxes'].shape[0] == 0:
                gt = None
            elif object_preds['boxes'].shape[0] == 0:
                gt = None
            else:
                weakest_link = self.get_weakest(object_preds)
                gt = self.get_ground_truth(object_target, weakest_link)
        return gt

    def get_prediction(self, gt, predictions):
        '''
        returns the label y ={1, 0} where y=1 if the label is the desired label, and -1 if the iou with
        the ground truth box is 0 (since the class has either flipped or is background). We also return the score, and the iou.
        ### THIS IS NOT A DIFFERENTIABLE FUNCTION ###
        '''
        obj_type = gt['labels'][0]
        object_preds = get_objects_of_type(predictions, obj_type, inc_scores=True)
        if len(object_preds['labels']) == 0:
            obj_iou = 0
            score = 0
            label = 0
        else:
            ious = torchvision.ops.box_iou(gt['boxes'], object_preds['boxes'].squeeze(dim=1))
            comparison_tensor = torch.zeros_like(ious)
            if torch.equal(comparison_tensor, ious):
                obj_iou = 0
                score = 0
                label = 0
            else:
                associated_pred_id = torch.argmax(ious, dim=1)
                associated_pred = {'boxes': object_preds['boxes'][associated_pred_id],
                                   'labels': object_preds['labels'][associated_pred_id],
                                   'scores': object_preds['scores'][associated_pred_id]}
                obj_iou = ious[0][associated_pred_id][0].item()
                label = 1
                score = object_preds['scores'][associated_pred_id][0].item()

        return obj_iou, score, label

    def generate_population(self, num_indiv, shape):
        # generate initial population
        population = torch.nn.init.normal_(torch.zeros((num_indiv, shape[0], shape[1], shape[2]), requires_grad=False),
                                           mean=self.init_pop_mean, std=self.init_pop_dev)
        return population

    def generate_offspring_asexual(self, population):
        # generate offspring for recombination and add random mutations
        new_population = []
        for i in range(self.num_offspring):
            new_population.append(population)
        new_population = torch.cat(new_population)
        mutations = torch.nn.init.normal_(torch.zeros_like(new_population, requires_grad=False), mean=self.mut_mean,
                                          std=self.mut_deviation)
        new_population = new_population + mutations
        new_population = torch.clamp(new_population, -self.max_val, self.max_val)
        return new_population

    # inp is tensor of shape C, W, H (no batch dimension)
    def evaluate_fitness(self, inp, gt, population):
        device = self.device
        # evaluate fitness of members of population
        self.model.eval()
        pop_fitness = []
        inp_tile = []
        for i in range(population.shape[0]):
            inp_tile.append(inp)
        inp_tile = torch.stack(inp_tile)
        perturbed_inp = inp_tile.cpu() + population
        perturbed_inp = [perturbed_inp[i].to(device) for i in range(perturbed_inp.shape[0])]
        model_preds = self.model(perturbed_inp)
        returned_labels = []
        for i in range(len(perturbed_inp)):
            iou, score, label = self.get_prediction(gt, model_preds[i])
            perturb = population[i]
            perturb = perturb.view(-1)
            pert_norm = torch.norm(perturb, p=np.inf)
            returned_labels.append(label)
            fitness = -pert_norm - (score * iou * label)
            pop_fitness.append(fitness)
        return torch.Tensor(pop_fitness), torch.Tensor(returned_labels)

    def reduce_population(self, population, fitness, ret_lab):
        remaining_pop = self.pop_reduction
        sorted_fitness, indices = torch.sort(fitness)
        if remaining_pop == None:
            remaining_pop = int(fitness.shape[0] / 2)
        asc_to_desc = torch.flip(indices, dims=[0])
        pop_by_fitness = population[asc_to_desc]
        lab_by_fitness = ret_lab[asc_to_desc]
        reduced_pop = pop_by_fitness[0:remaining_pop]
        reduced_lab = lab_by_fitness[0:remaining_pop]
        return reduced_pop, reduced_lab

    def attack(self, x, y, verbose=True):
        '''
        model takes as input list of tensors and returns a list containing dictionaries with the appropriate keys.
        x is a tensor of shape C W H with no batch dimension (single image at a time)
        y are the annotations for x converted to the appropriate format
        '''
        init_preds = self.model([x])[0]
        if y == None:
            y = init_preds
        gt = self.find_vulnerable(init_preds, y, self.attack_class)
        if gt == None:
            return None, None, None
        population = self.generate_population(self.init_pop_size, x.shape)
        for i in range(self.iterations):
            population = self.generate_offspring_asexual(population)
            fit, returned_labs = self.evaluate_fitness(x, gt, population)
            if verbose == True:
                av_fitness = torch.mean(fit)
                print('average fitness at generation {}: '.format(i), av_fitness.item())
            if torch.max(fit) > -self.thresh:
                population, labs = self.reduce_population(population, fit, returned_labs)
                break
            population, labs = self.reduce_population(population, fit, returned_labs)
        negated = torch.where(labs == 0, labs, torch.tensor([-1.0]).float()[0])
        flipped_locs = negated == -1
        flipped_idx = negated.nonzero()
        if flipped_idx.nelement() > 0:
            population = population[flipped_idx]

        outs = population[0]
        if len(outs.shape) > 3:
            outs = outs[0]
        return outs, gt, init_preds


def get_conf_preds(output_dict, thresh=0.6):
    # returns indices of most confident predictions
    scores = output_dict['scores']
    scores_above_thresh = scores >= thresh
    indices = scores_above_thresh.nonzero()
    return torch.squeeze(indices, dim=1)


def detect_dict_from_idx(inp_dict, ids):
    key_list = list(inp_dict.keys())
    new_dict = {}
    for key in key_list:
        new_dict[key] = inp_dict[key][ids]
    return new_dict


def check_detections(conf_preds, target, thresh=0.5):
    # finds fp tp in predictions
    pred_boxes = conf_preds['boxes']
    pred_labels = conf_preds['labels']
    pred_scores = conf_preds['scores']

    true_boxes = target['boxes']
    true_labels = target['labels']

    # fp is represented as 0, tp is represented as 1
    fp_tp = []
    # ground truth elements with corresponding prediction
    taken_indices = []

    for idx in range(pred_labels.shape[0]):
        current_class = pred_labels[idx]
        true_examples = true_labels == current_class
        example_indices = true_examples.nonzero()
        if example_indices.nelement() == 0:
            # no elements in gt of corresponding type
            fp_tp.append(0)
        else:
            obj_boxes = true_boxes[example_indices]
            cur_pred_box = pred_boxes[idx]
            ious = torchvision.ops.box_iou(obj_boxes.squeeze(dim=1), cur_pred_box.unsqueeze(dim=0))
            detects = ious >= thresh
            if detects.nelement() > 0:
                val, max_idx = torch.max(ious, dim=0)
                fp_tp.append(1)
                taken_indices.append(example_indices[max_idx[0]])
                if detects.nelement() > 1:
                    for i in range(detects.nelement() - 1):
                        fp_tp.append(0)
            else:
                fp_tp.append(0)
    return fp_tp, torch.cat(taken_indices)


def get_fn(targs, taken_inds):
    # returns num false negatives
    taken_inds = torch.unique(taken_inds)
    labs = targs['labels']
    fn = labs.shape[0] - taken_inds.shape[0]
    return fn


def precision_recall(ftp_list, fn_count):
    counted = Counter(ftp_list)
    tp = counted[1]
    fp = counted[0]
    prec = tp / (tp + fp)
    rec = tp / (tp + fn_count)
    return prec, rec


def pr_curve(pred_dict, target_dict, step_size=0.1, iou_thresh=0.5):
    vals = np.arange(0.1, 0.99, step_size).tolist()
    prec = []
    rec = []
    thresh = []
    for val in vals:
        idx_at_thresh = get_conf_preds(pred_dict, val)
        conf_dict = detect_dict_from_idx(pred_dict, idx_at_thresh)
        ftp_list, indxs = check_detections(conf_dict, target_dict, iou_thresh)
        fn_counts = get_fn(target_dict, indxs)
        pre, re = precision_recall(ftp_list, fn_counts)
        prec.append(pre)
        rec.append(re)
        # checking consistency with vals
        thresh.append(val)
    return prec, rec, thresh


def mAP(pred_dict, target_dict, step_size=0.1, iou_thresh=0.5):
    if pred_dict['labels'].shape[0] == 0:
        return 0
    prec, rec, thresh = pr_curve(pred_dict, target_dict, step_size=step_size, iou_thresh=iou_thresh)
    combined = list(zip(rec, prec))
    combined.sort()
    prec = [x for y, x in combined]
    rec = [y for y, x in combined]
    sum_list = []
    for idx in range(len(rec) - 1):
        pinterp = max(prec[idx + 1:])
        coeff = rec[idx + 1] - rec[idx]
        sum_list.append(pinterp * coeff)
    return sum(sum_list)


def check_flip(predictions, ground_truth, obj_cat, iou_thresh=0.5, nms_thresh=0.05):
    # assume non-nms preds. flip=1 means succesful attack, flip=0 means unsuccesful
    # pred_ids = torchvision.ops.nms(predictions['boxes'], predictions['scores'], nms_thresh)
    nms_reduced_preds = predictions  # detect_dict_from_idx(predictions, pred_ids)
    reduced_preds = get_objects_of_type(nms_reduced_preds, obj_cat)
    if reduced_preds['boxes'].nelement() == 0:
        flip = 1
        return flip, nms_reduced_preds
    ious = torchvision.ops.box_iou(ground_truth['boxes'], reduced_preds['boxes'].squeeze(dim=1))
    flip = 1
    if torch.max(ious) >= iou_thresh:
        flip = 0
    return flip


def nms_pred_reduce(predictions, nms_thresh=0.05):
    pred_ids = torchvision.ops.nms(predictions['boxes'], predictions['scores'], nms_thresh)
    nms_reduced_preds = detect_dict_from_idx(predictions, pred_ids)
    return nms_reduced_preds