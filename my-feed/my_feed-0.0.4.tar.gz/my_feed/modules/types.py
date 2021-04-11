from enum import Enum


class PostType(Enum):
    """
    Types of post
    """
    EMBED = 'Embed'
    IMAGE = 'Image'
    VIDEO = 'Video'
    TEXT = 'Text'
    NONE = None

    @staticmethod
    def type_by_id(type_id: str):
        """
        Check if the GenderItem is in Type
        :param type_id:
        :return:
        """
        items_list = [
            attr for attr in dir(PostType) if not callable(getattr(PostType, attr)) and not attr.startswith("__")
        ]
        for attr in items_list:
            if type_id == getattr(PostType, attr).value[0]:
                return getattr(PostType, attr)
        return PostType.NONE
