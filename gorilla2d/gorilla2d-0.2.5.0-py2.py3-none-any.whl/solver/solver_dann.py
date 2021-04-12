# Copyright (c) Gorilla-Lab. All rights reserved.
import torch
import time
import os
import numpy as np

from gorilla.solver import BaseSolver
from gorilla.solver import save_summary, adjust_learning_rate
from torch.nn import CrossEntropyLoss
from gorilla.utils import Timer

class solver_DANN(BaseSolver):
    def __init__(self,
                 model,
                 dataloaders,
                 evaluator,
                 cfg,
                 logger=None):
        # next line is only used for InvLR scheduler
        cfg.lr_scheduler.update(
            {"maxp": cfg.pop("max_iters", cfg.epochs * cfg.iters_per_epoch)})
        super().__init__(model, dataloaders, cfg, logger)
        checkpoint = cfg.get("checkpoint", "")
        if checkpoint:
            self.resume(checkpoint) # resume model, optimizer and lr_scheduler
        self.evaluator = evaluator
        self.criterions = {"CELoss": torch.nn.CrossEntropyLoss()}
        self.best_acc = 0
        self.timer = Timer()

    def solve(self):
        print("Begin training")
        tmp = int(self.epoch) # for deep copy
        self.epoch = -1
        self.evaluate()
        self.epoch = tmp
        print(len(self.dataloaders["train_src"]), len(self.dataloaders["train_tgt"]), len(self.dataloaders["test_tgt"]))
        while self.epoch < self.cfg.epochs:
            self.train()

            if self.epoch % self.cfg.test_interval == (self.cfg.test_interval - 1):
                self.evaluate()

            self.epoch += 1

    def get_ready(self):
        # initialize data iterators
        data_iterators = {}
        for key in self.dataloaders.keys():
            data_iterators[key] = iter(self.dataloaders[key])
        self.data_iterators = data_iterators

        self.iters_per_epoch = self.cfg.pop("iters_per_epoch", len(self.dataloaders["train_src"]))
        self.max_iters = self.cfg.epochs * self.iters_per_epoch

    def get_samples(self, data_name):
        assert data_name in self.dataloaders

        data_loader = self.dataloaders[data_name]
        data_iterator = self.data_iterators[data_name]
        assert data_loader is not None and data_iterator is not None, \
            "Check your dataloader of %s." % data_name

        try:
            sample = next(data_iterator)
        except StopIteration:
            data_iterator = iter(data_loader)
            sample = next(data_iterator)
            self.data_iterators[data_name] = data_iterator
        return sample

    def train(self):
        self.model.train()
        self.log_buffer.clear()

        go_on = True
        while go_on:
            self.timer.reset()
            # prepare the data for the model forward and backward
            # note that DANN is used on the condition that the label of
            # target dataset is not available
            source_data, source_gt, _ = self.get_samples("train_src")
            target_data, _, _ = self.get_samples("train_tgt")

            if torch.cuda.is_available():
                source_data = source_data.cuda()
                source_gt = source_gt.cuda()
                target_data = target_data.cuda()

            self.log_buffer.update({"data_time": self.timer.since_start()})
            # prepare domain labels
            domain_labels_source = torch.zeros((source_data.size()[0])).type(torch.LongTensor)
            domain_labels_target = torch.ones((target_data.size()[0])).type(torch.LongTensor)
            if torch.cuda.is_available():
                domain_labels_source = domain_labels_source.cuda()
                domain_labels_target = domain_labels_source.cuda()

            # compute the output of source domain and target domain
            outputs = self.model(source_data, target_data, self.iter)

            # compute the category loss of feature_source
            loss_C = self.criterions["CELoss"](outputs["cate_src"], source_gt)
            # compute the domain loss of feature_source and target_feature
            domain_loss_source = self.criterions["CELoss"](outputs["domain_src"], domain_labels_source)
            domain_loss_target = self.criterions["CELoss"](outputs["domain_tgt"], domain_labels_target)
            loss_G = domain_loss_target + domain_loss_source

            loss_total = loss_C + loss_G
            self.log_buffer.update(
                dict(
                    loss_total=loss_total.item(),
                    loss_C=loss_C.item(),
                    loss_G=loss_G.item(),
                ))

            self.optimizer.zero_grad()
            loss_total.backward()
            self.optimizer.step()

            self.evaluator.process(outputs["cate_src"], source_gt)

            self.log_buffer.update({"batch_time": self.timer.since_start()})

            if self.iter % self.cfg.log_interval == self.cfg.log_interval - 1:
                acc = self.evaluator.evaluate()[0]
                self.evaluator.reset()

                self.log_buffer.average(self.cfg.log_interval)
                out_tmp = self.log_buffer.output
                log_string = ("Tr ep [{}/{}] it [{}/{}]  BT {:.3f}  DT {:.3f}   S@1 {:.3f}\n"
                              "loss_total {:.3f}   loss_C {:.3f}   loss_G {:.3f}").format(
                            self.epoch, self.cfg.epochs,
                            self.iter % self.iters_per_epoch + 1, self.iters_per_epoch,
                            out_tmp["batch_time"], out_tmp["data_time"], acc,
                            out_tmp["loss_total"], out_tmp["loss_C"], out_tmp["loss_G"])
                self.logger.info(log_string)

                self.tb_writer.add_scalars(
                    "loss", {
                        "total": out_tmp["loss_total"],
                        "loss_C": out_tmp["loss_C"],
                        "loss_G": out_tmp["loss_G"],
                    }, self.iter)
                self.tb_writer.add_scalars(
                    "acc", {"train": acc},
                    self.iter)

                # save checkpoint every some epochs
                if self.epoch % self.cfg.save_interval == (self.cfg.save_interval - 1):
                    filepath = os.path.join("log", "summary.npy")
                    state = {
                        "epoch": self.epoch,
                        "arch": self.cfg.arch,
                        "loss": loss_total,
                        "optimizer": self.optimizer.state_dict(),
                        "model": self.model.state_dict()
                    }
                    filename = "latest_model.pth.tar"
                    dir_save_file = os.path.join(self.cfg.log, filename)

                    save_summary(filepath, state, dir_save_file, loss_total, desc="loss in self.epoch {}".format(self.epoch), smaller=True, overwrite=True)

            if self.iter % self.iters_per_epoch == self.iters_per_epoch - 1:
                go_on = False
            self.iter += 1
            self.lr_scheduler.step()
            # for param_group in self.optimizer.param_groups:
            #     print(self.iter, "lr of {}".format(param_group["name"]), param_group["lr"])

    def evaluate(self):
        self.model.eval()
        self.log_buffer.clear()

        self.timer.reset()
        with torch.no_grad():
            for _, data in enumerate(self.dataloaders["test_tgt"]):
                target_data, target_gt, _ = data
                if torch.cuda.is_available():
                    target_data = target_data.cuda()
                    target_gt = target_gt.cuda()

                outputs_target = self.model.forward_test(target_data)["cate_tgt"]

                self.evaluator.process(outputs_target, target_gt)
        acc = self.evaluator.evaluate()[0]
        self.evaluator.reset()

        print_string = ("Te self.epoch [{}/{}]  Time {:.3f}   Target acc {:.3f}").format(
            self.epoch, self.cfg.epochs, self.timer.since_last(), acc)
        self.logger.info(print_string + "\n")

        if self.best_acc < acc:
            self.best_acc = acc
            filepath = os.path.join("log", "summary.npy")
            state = {
                "epoch": self.epoch,
                "arch": self.cfg.arch,
                "best_acc": acc,
                "model": self.model.state_dict()
            }
            filename = "best_model.pth.tar"
            dir_save_file = os.path.join(self.cfg.log, filename)
            save_summary(filepath, state, dir_save_file, self.best_acc, desc="best_prec1", smaller=False)

        self.tb_writer.add_scalars(
            "acc", {
                "test": acc,
                "best_prec1": self.best_acc
            }, self.iter)
