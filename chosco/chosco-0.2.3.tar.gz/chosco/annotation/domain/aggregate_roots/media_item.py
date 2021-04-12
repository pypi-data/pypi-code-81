from typing import Dict


class MediaItem(object):
    def __init__(self, media_id: str, media_bucket: str = None, metadata: Dict = None):
        self.media_id = media_id
        self.media_bucket = media_bucket
        self.metadata = metadata

    def __eq__(self, other):
        return self.media_id == other.media_id

    def to_dict(self) -> Dict:
        return dict(
            media_id=self.media_id,
            media_bucket=self.media_bucket,
            metadata=self.metadata,
        )

    @staticmethod
    def from_dict(media_item_dict: Dict):
        media_id = media_item_dict.get("media_id")
        media_bucket = media_item_dict.get("media_bucket", None)
        metadata = media_item_dict.get("metadata", None)
        return MediaItem(media_id, media_bucket, metadata)
