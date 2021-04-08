import torch
import torch.distributed as dist
import oss2
import os
import time
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def init_oss():
    oss_path = "aop/pytorch/%s/" % os.environ['WORKFLOW_ID']
    oss_hint_path = oss_path + "hint"
    auth = oss2.Auth(os.environ['OSS_ACCESS_ID'], os.environ['OSS_ACCESS_KEY'])
    bucket = oss2.Bucket(auth, os.environ['OSS_ENDPOINT'], os.environ['OSS_BUCKET'])

    return oss_path, oss_hint_path, auth, bucket

def save_model(model_name, model, hint=None, max_checkpoint=1):
    """
    save checkpoint to oss path oss://bucket/aop/pytorch/{workflowId}/{yymmddhhMMss}/{model_name}.pth

    :param model_name: model's name, if there are multi models, you must ensure model name is unique.
    :param model: model, can be instance of torch.nn.DataParallel or torch.nn.parallel.DistributedDataParallel or state_dict
    :param hint: dict type , save your hint data to oss, example: {"epoch": 2}
    :param max_checkpoint: max num of checkpoint
    """
    try:
        if dist.get_rank() == 0:
            oss_path, oss_hint_path, auth, bucket = init_oss()
            current_time = time.strftime("%Y%m%d%H", time.localtime(time.time()))
            oss_model_path = oss_path + "%s/%s.pth" % (current_time, model_name)

            # delete surplus directory
            exist_ckpt = bucket.list_objects(prefix=oss_path, delimiter='/').prefix_list
            if len(exist_ckpt) >= max_checkpoint:
                exist_ckpt.sort()
                for i in range(len(exist_ckpt) - max_checkpoint):
                    for obj in oss2.ObjectIterator(bucket, prefix=exist_ckpt[i]):
                        bucket.delete_object(obj.key)

            logger.info("start to save checkpoint %s to %s." % (model_name, oss_model_path))
            retry_times = 3
            while retry_times > 0:
                try:
                    buffer = BytesIO()
                    if any(isinstance(model, x) for x in
                           [torch.nn.DataParallel, torch.nn.parallel.DistributedDataParallel]):
                        torch.save(model.module.state_dict(), buffer)
                    else:
                        torch.save(model.state_dict(), buffer)

                    bucket.put_object(oss_model_path, buffer.getvalue())
                    buffer.close()
                    bucket.put_object(oss_hint_path, str(hint))
                    return
                except IOError:
                    retry_times -= 1
                    logger.info("save checkpoint failed, retry...")

    except Exception as e:
        logger.error("save checkpoint failed %s." % str(e))


def load_model(model_name, model, device=torch.device("cuda")):
    """
    load checkpoint from oss path oss://bucket/aop/pytorch/{workflowId}/{yymmddhhMMss}/{model_name}.pth

    :param model_name: model's name, if there are multi models, you must ensure model name is unique.
    :param model: model, can be instance of torch.nn.DataParallel or torch.nn.parallel.DistributedDataParallel or state_dict
    :param device: device type , torch.device("cuda") or torch.device("cpu")
    """
    try:
        oss_path, oss_hint_path, auth, bucket = init_oss()
        if len(bucket.list_objects(prefix=oss_path, delimiter='/').prefix_list) == 0:
            logger.info("no checkpoint for model %s, skipped." % model_name)
            return

        # select the latest directory
        exist_ckpt = bucket.list_objects(prefix=oss_path, delimiter='/').prefix_list
        exist_ckpt.sort()
        oss_model_real_path = exist_ckpt[len(exist_ckpt) - 1]
        oss_model_path = oss_model_real_path + "%s.pth" % model_name

        logger.info("start to load checkpoint %s from %s." % (model_name, oss_model_path))
        retry_times = 3
        while retry_times > 0:
            try:
                buffer = BytesIO(bucket.get_object(oss_model_path).read())
                state_dict = torch.load(buffer, map_location=device)

                if isinstance(model, torch.nn.DataParallel) or isinstance(model,
                                                                          torch.nn.parallel.DistributedDataParallel):
                    model.module.load_state_dict(state_dict)
                else:
                    model.load_state_dict(state_dict)

                return
            except IOError:
                retry_times -= 1
                logger.info("load checkpoint failed, retry...")

    except Exception as e:
        logger.error("save checkpoint failed %s." % str(e))


def get_hint():
    """
    get epoch from oss path oss://bucket/aop/pytorch/{workflowId}/hint

    :return: hint, a dict type, example: {"epoch": "1"}
    """
    try:
        oss_path, oss_hint_path, auth, bucket = init_oss()
        if len(bucket.list_objects(prefix=oss_path, delimiter='/').prefix_list) == 0:
            return {}

        logger.info("start to get epoch from %s." % oss_hint_path)
        retry_times = 3
        while retry_times > 0:
            try:
                hint = str(bucket.get_object(oss_hint_path).read(), encoding="utf-8")
                logger.info("get hint is %s." % hint)
                return eval(hint)
            except IOError:
                retry_times -= 1
                logger.info("get epoch failed, retry...")
    except Exception as e:
        logger.error("get hint failed %s." % str(e))
