import asyncio
import logging
import os
import rospy

_logger = logging.getLogger("arospy.client")


async def spin():
    """
    Wait until ROS node is shutdown. Yields activity to other threads.
    @raise ROSInitException: if node is not in a properly initialized state
    """

    if not rospy.core.is_initialized():
        raise rospy.exceptions.ROSInitException("client code must call rospy.init_node() first")
    _logger.debug("node[%s, %s] entering spin(), pid[%s]", rospy.core.get_caller_id(), rospy.core.get_node_uri(),
                  os.getpid())
    while not rospy.core.is_shutdown():
        await asyncio.sleep(0.5)
