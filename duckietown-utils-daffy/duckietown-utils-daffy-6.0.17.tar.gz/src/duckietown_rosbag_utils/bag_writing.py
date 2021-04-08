import os
from contextlib import contextmanager

import duckietown_code_utils as dtu
import rosbag
from . import logger

__all__ = ["d8n_write_to_bag_context"]


@contextmanager
def d8n_write_to_bag_context(out_bag_filename):
    """
    with d8n_write_to_bag_context(filename) as bag:
        bag.write(topic_name, msg)

    """

    dtu.d8n_make_sure_dir_exists(out_bag_filename)
    out_bag = rosbag.Bag(out_bag_filename + ".tmp", "w")
    yield out_bag
    out_bag.close()
    os.rename(out_bag_filename + ".tmp", out_bag_filename)
    logger.info("Written bag to %s" % out_bag_filename)
