from typing import Union

from PIL import ImageFile

import duckietown_code_utils as dtu
from cv_bridge import CvBridge

from sensor_msgs.msg import CompressedImage, Image


class ImageConversions:
    # We only instantiate the bridge once
    bridge: CvBridge = None


def get_cv_bridge() -> CvBridge:
    if ImageConversions.bridge is None:

        ImageConversions.bridge = CvBridge()
    return ImageConversions.bridge


def rgb_from_imgmsg(msg: Image) -> dtu.NPImageRGB:
    bridge = get_cv_bridge()
    return bridge.imgmsg_to_cv2(msg, "rgb8")


def bgr_from_imgmsg(msg: Image) -> dtu.NPImageBGR:
    bridge = get_cv_bridge()
    return bridge.imgmsg_to_cv2(msg, "bgr8")


def d8n_image_msg_from_cv_image(cv_image: dtu.NPImage, image_format, same_timestamp_as=None):
    """
    Makes an Image message from a CV image.

    if same_timestamp_as is not None, we copy the timestamp
    from that image.

    image_format: 'bgr8' or 'mono' or similar
    """
    bridge = get_cv_bridge()
    image_msg_out = bridge.cv2_to_imgmsg(cv_image, image_format)
    if same_timestamp_as is not None:
        image_msg_out.header.stamp = same_timestamp_as.header.stamp
    return image_msg_out


def pil_from_CompressedImage(msg: CompressedImage):
    parser = ImageFile.Parser()
    parser.feed(msg.data)
    res = parser.close()
    return res


def rgb_from_ros(msg: Union[CompressedImage, Image]) -> dtu.NPImageRGB:
    if "CompressedImage" in msg.__class__.__name__:
        return dtu.rgb_from_pil(pil_from_CompressedImage(msg))
    else:
        return rgb_from_imgmsg(msg)


numpy_from_ros_compressed = rgb_from_ros
