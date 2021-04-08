import logging

logger = logging.getLogger("duckietown_utils_rosbag")
logger.setLevel(logging.DEBUG)

try:
    import rosbag
except ImportError:
    logger.warn("Could not import rosbag; disabling ROS utils")
else:

    from .bag_info import *
    from .bag_logs import *
    from .bag_reading import *
    from .bag_visualization import *
    from .bag_writing import *
