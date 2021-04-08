import os
import re
import subprocess
from typing import List, NewType, Tuple, Union

import rosbag
from duckietown_code_utils import get_cached, yaml_load_plain
from sensor_msgs.msg import CameraInfo
from . import logger
from .bag_reading import BagReadProxy

__all__ = [
    "rosbag_info",
    "rosbag_info_cached",
    "d8n_get_all_images_topic_bag",
    "d8n_get_all_images_topic",
    "which_robot",
    "get_image_topic",
    "read_camera_info_from_bag",
]

BagInfoDict = NewType("BagInfoDict", dict)


def rosbag_info_cached(filename: str) -> BagInfoDict:
    def f():
        return rosbag_info(filename)

    basename = os.path.basename(filename)
    cache_name = "rosbag_info/" + basename
    return get_cached(cache_name, f, quiet=True)


def rosbag_info(bag: str) -> BagInfoDict:
    msg = f"rosbag_info {bag}"
    logger.debug(msg)
    stdout = subprocess.Popen(["rosbag", "info", "--yaml", bag], stdout=subprocess.PIPE).communicate()[0]
    stdout = stdout.decode()
    info_dict = yaml_load_plain(stdout)
    return info_dict


def which_robot(bag: Union[rosbag.Bag, BagReadProxy]) -> str:
    pattern = r"/(\w+)/camera_node/image/compressed"

    topics = list(bag.get_type_and_topic_info()[1].keys())

    for topic in topics:
        m = re.match(pattern, topic)
        if m:
            vehicle = m.group(1)
            return vehicle
    msg = "Could not find a topic matching %s" % pattern
    raise ValueError(msg)


def get_image_topic(bag: Union[rosbag.Bag, BagReadProxy]) -> str:
    """ Returns the name of the topic for the main camera """
    topics = list(bag.get_type_and_topic_info()[1].keys())
    for t in topics:
        if "camera_node/image/compressed" in t:
            return t
    msg = "Cannot find the topic: %s" % topics
    raise ValueError(msg)


def d8n_get_all_images_topic(bag_filename: str) -> List[Tuple[str, type]]:
    """
    Returns the (name, type) of all topics that look like images.
    """

    bag = rosbag.Bag(bag_filename)
    return d8n_get_all_images_topic_bag(bag)


def d8n_get_all_images_topic_bag(bag: rosbag.Bag, min_messages: int = 0) -> List[Tuple[str, type]]:
    """
    Returns the (name, type) of all topics that look like images
    and that have nonzero message count.
    """
    tat = bag.get_type_and_topic_info()
    consider_images = [
        "sensor_msgs/Image",
        "sensor_msgs/CompressedImage",
    ]
    all_types = set()
    found = []
    topics = tat.topics
    for t, v in list(topics.items()):
        msg_type = v.msg_type
        all_types.add(msg_type)
        message_count = v.message_count
        if msg_type in consider_images:

            # quick fix: ignore image_raw if we have image_compressed version
            if "raw" in t:
                other = t.replace("raw", "compressed")

                if other in topics:
                    continue

            if message_count < min_messages:
                # print('ignoring topic %r because message_count = 0' % t)
                continue

            found.append((t, msg_type))
    return found


def read_camera_info_from_bag(bag_in: BagReadProxy) -> CameraInfo:
    from .bag_reading import MessagePlus

    m: MessagePlus
    for m in bag_in.read_messages_plus():
        if "camera_info" in m.topic:
            return m.msg
    msg = "Could not find any camera_info message."
    raise ValueError(msg)
