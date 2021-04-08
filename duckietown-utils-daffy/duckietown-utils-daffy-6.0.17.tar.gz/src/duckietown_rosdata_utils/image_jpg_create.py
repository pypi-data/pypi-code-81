import cv2
import numpy as np

from sensor_msgs.msg import CompressedImage
import duckietown_code_utils as dtu

__all__ = [
    "d8_compressed_image_from_cv_image",
]


def d8_compressed_image_from_cv_image(
    image_cv: dtu.NPImageBGR, same_timestamp_as=None, timestamp=None
) -> CompressedImage:
    """
    Create CompressedIamge from a CV BGR image.

    TODO: assumptions on format?
    """

    compress = cv2.imencode(".jpg", image_cv)[1]
    jpg_data = np.array(compress).tostring()
    msg = CompressedImage()

    if same_timestamp_as is not None:
        msg.header.stamp = same_timestamp_as.header.stamp
    elif timestamp is not None:
        msg.header.stamp = timestamp
    else:
        from rospy import Time

        msg.header.stamp = Time.now()
    msg.format = "jpeg"
    msg.data = jpg_data
    return msg
