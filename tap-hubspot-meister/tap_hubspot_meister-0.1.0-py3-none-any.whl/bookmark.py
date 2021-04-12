import singer
from singer import utils

LOGGER = singer.get_logger()


def get_bookmark(self, state):
    if self.replication_method == "INCREMENTAL" and (
        (
            state is None
            or "bookmarks" not in state
            or not state.get("bookmarks", {})
            .get(self.name, {})
            .get(self.replication_key)
        )
    ):
        LOGGER.info("No bookmark found for the stream {}".format(self.name))
        bookmark = utils.strptime_with_tz(self.config["start_date"])
    else:
        bookmark = self.get_bookmark(state)

    LOGGER.info(
        "stream: {}, bookmark_field: {}, last_datetime: {}".format(
            self.name, self.replication_key, bookmark
        )
    )
    return bookmark
