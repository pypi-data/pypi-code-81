from . import TrojEpsilon
import numpy as np
import pandas as pd
from . import array_utils
from . import attack_utils
from . import ODAttack
import torch


class BasicRobustnessEvaluator:
    def __init__(
        self,
        classifier,
        learning_rate=0.01,
        eps_steps=0.05,
        max_halving=10,
        max_doubling=10,
        num_iters=15,
        batch_size=128,
        norm=np.inf,
        k=5,
    ):
        self.classifier = classifier
        self.attacker = TrojEpsilon.TrojEpsAttack(
            self.classifier,
            learning_rate=learning_rate,
            eps_steps=eps_steps,
            max_halving=max_halving,
            max_doubling=max_doubling,
            num_iters=num_iters,
            batch_size=batch_size,
            norm=norm,
            k=k,
        )

    def attack(self, data, target, index, device=None):
        """
        This will work for pytorch, tensorflow has no device
        """
        # index = index.numpy()
        # send data and target to cpu, convert to numpy
        data = np.ascontiguousarray(data.astype(np.float32))
        preds = self.classifier.predict(data)
        preds = np.argmax(preds, axis=1)
        self.classifier._reduce_labels = False

        test_loss = self.classifier.loss(data, target, reduction="none")
        self.classifier._reduce_labels = True
        adv_x = self.attacker.generate(data, target)
        adv_preds = self.classifier.predict(adv_x)
        self.classifier._reduce_labels = False
        adv_loss = self.classifier.loss(adv_x, target, reduction="none")
        perturbation = array_utils.compute_Lp_distance(data, adv_x)
        adv_pred = np.argmax(adv_preds, axis=1)
        # generate the adversarial image using the data numpy array and label numpy array
        out_dict = {
            "Linf_perts": perturbation,
            "Loss": test_loss,
            "Adversarial_Loss": adv_loss,
            "prediction": preds,
            "Adversarial_prediction": adv_pred,
        }
        return (out_dict, index)



class BlackBoxODEvaluator:
    #different run form to classification
    def __init__(self, model, obj_class, loader, batch_iterator, df=None, device='cuda',
                 iou_thresh=0.5, nms_thresh=0.05, step_size=0.1, verbose=True, **attkwargs):
        self.model = model
        self.obj_class = obj_class
        self.loader = loader
        self.batch_iterator = batch_iterator
        self.df = df
        if self.df == None:
            self.df = loader.dataframe
        self.device = device
        self.iou_thresh = iou_thresh
        self.nms_thresh = nms_thresh
        self.step_size = step_size
        self.attacker = ODAttack.EvoDAttack(self.model, self.obj_class, **attkwargs)
        self.verbose = verbose

    def run(self, num_samples):
        tracker = 0
        attacked_ids = []
        batch_enum = enumerate(self.batch_iterator)
        while tracker <= num_samples:
            batch_id, (ims, labs, ids) = next(batch_enum)
            if tracker > 0 and batch_id == 0:
                break
            for idx in range(len(labs)):
                sample_id = ids[idx]
                perturb, gt, preds = self.attacker.attack(ims[idx], labs[idx])
                if gt == None:
                    continue
                else:
                    pert_im = ims[idx] + perturb.to(self.device)
                    pert_preds = self.model([pert_im])[0]
                    nms_pert_preds = ODAttack.nms_pred_reduce(pert_preds, self.nms_thresh)
                    nms_preds = ODAttack.nms_pred_reduce(preds, self.nms_thresh)
                    flip = ODAttack.check_flip(nms_pert_preds, gt, self.obj_class, self.iou_thresh, self.nms_thresh)
                    troj_map = ODAttack.mAP(nms_preds, labs[idx], self.step_size, self.iou_thresh)
                    adv_troj_map = ODAttack.mAP(nms_pert_preds, labs[idx], self.step_size, self.iou_thresh)
                    pert_vec = perturb.view(-1)
                    linf_pert = torch.norm(pert_vec, p=np.inf)
                    tracker += 1
                    data_dict = {'flip':flip, 'TmAP':troj_map, 'Adv_TmAP':adv_troj_map, 'Linf':linf_pert.item()}
                    self.df = attack_utils.log_to_dataframe(self.df, sample_id, data_dict)
                    attacked_ids.append(sample_id)
        return self.df, attacked_ids

