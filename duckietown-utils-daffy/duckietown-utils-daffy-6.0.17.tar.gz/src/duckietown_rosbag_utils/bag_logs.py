import os
from typing import Optional

import numpy as np

import rosbag
import duckietown_code_utils as dtu
from duckietown_rosdata_utils.image_conversions import rgb_from_ros
from . import logger
from .bag_info import get_image_topic
from .bag_reading import BagReadProxy

__all__ = [
    "d8n_read_images_interval",
    "d8n_read_all_images",
    "d8n_read_all_images_from_bag",
]


def d8n_read_images_interval(filename: str, t0: Optional[float], t1: Optional[float]):
    """
    Reads all the RGB data from the bag,
    in the interval [t0, t1], where t0 = 0 indicates
    the first image.

    """
    data = d8n_read_all_images(filename, t0, t1)
    logger.info(f"Read {len(data)} images from {filename}.")
    timestamps = data["timestamp"]
    # normalize timestamps
    first = data["timestamp"][0]
    timestamps -= first
    logger.info(f"Sequence has length {timestamps[-1]:.2f} seconds.")
    return data


def d8n_read_all_images(filename: str, t0: Optional[float] = None, t1: Optional[float] = None):
    """
    Raises a ValueError if no data could be read.

    Returns a numpy array.


    Usage:

        data = d8n_read_all_images(bag)

        print data.shape # (928,)
        print data.dtype # [('timestamp', '<f8'), ('rgb', 'u1', (480, 640, 3))]

    """

    filename = dtu.expand_environment(filename)
    if not os.path.exists(filename):
        msg = f"File does not exist: {filename!r}"
        raise ValueError(msg)
    bag = rosbag.Bag(filename)
    topic = get_image_topic(bag)
    bag_proxy = BagReadProxy(bag, t0, t1)
    res = d8n_read_all_images_from_bag(bag_proxy, topic)
    bag_proxy.close()
    return res


def d8n_read_all_images_from_bag(bag, topic0, max_images=None, use_relative_time=False):
    nfound = bag.get_message_count(topic_filters=topic0)
    logger.info(f"Found {nfound} images for {topic0}")

    data = []
    first_timestamp = None

    if max_images is None:
        interval = None
    else:
        interval = int(np.ceil(nfound / max_images))
        if interval == 0:
            interval = 1
        logger.info(f"There are nfound = {nfound} images total and I want max_images = {max_images}")
        logger.info(f"Therefore I will use interval = {interval}")

    rgb = None
    for j, (topic, msg, t) in enumerate(bag.read_messages(topics=[topic0])):

        float_time = t.to_sec()

        if use_relative_time:
            float_time = float_time - bag.get_start_time()
        if first_timestamp is None:
            first_timestamp = float_time

        if interval is not None:
            add = j % interval == 0
            if not add:
                continue

        rgb = rgb_from_ros(msg)

        data.append({"timestamp": float_time, "rgb": rgb})

        # stop if we have enough images
        if max_images is not None and (len(data) >= max_images):
            break

        if j % 10 == 0:
            logger.debug(f"Read {j} images from topic {topic}")

    logger.info(f"Returned {len(data)} images")
    if not data:
        msg = f"No data found for topic {topic0}"
        raise ValueError(msg)

    H, W, _ = rgb.shape  # (480, 640, 3)
    logger.info(f"Detected image shape: {W} x {H}")
    n = len(data)

    dtype = [
        ("timestamp", "float"),
        ("rgb", "uint8", (H, W, 3)),
    ]

    x = np.zeros((n,), dtype=dtype)

    for i, v in enumerate(data):
        x[i]["timestamp"] = v["timestamp"]
        x[i]["rgb"][:] = v["rgb"]

    return x
