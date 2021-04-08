import pynvml
from loguru import logger
import traceback


def check_gpu(mem_required):
    """
    检查满足内存要求的gpu
    :param mem_required: 内存要求（M）
    :return:gpu编号列表
    """
    try:
        pynvml.nvmlInit()
    except pynvml.NVMLError:
        logger.error('gpu init error:{}'.format(traceback.format_exc()))
        return []

    gpu_idx_list = []
    for gpu_idx in range(pynvml.nvmlDeviceGetCount()):
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_idx)
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        mem_total, mem_free = mem_info.total / 1024 / 1024, mem_info.free / 1024 / 1024
        logger.info('gpu:{},mem_total:{}, mem_free:{}'.format(gpu_idx, mem_total, mem_free))
        if mem_free > mem_required:
            logger.info('gpu:{} is matched'.format(gpu_idx))
            gpu_idx_list.append(gpu_idx)
    logger.info('match gpus:{}',gpu_idx_list)
    return gpu_idx_list
