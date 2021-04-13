import singer

from streams import STREAMS

LOGGER = singer.get_logger()


def sync(client, config, catalog, state):
    # Get selected_streams from catalog, based on state last_stream
    # last_stream = Previous currently synced stream, if the load was interrupted
    last_stream = singer.get_currently_syncing(state)
    LOGGER.info("last/currently syncing stream: {}".format(last_stream))
    selected_streams = []
    for stream in catalog.get_selected_streams(state):
        selected_streams.append(stream.stream)
    LOGGER.info("selected_streams: {}".format(selected_streams))

    # If there's nothing to sync, return
    if not selected_streams or selected_streams == []:
        return

    for stream_name, stream in STREAMS.items():
        if stream_name in selected_streams:
            LOGGER.info("current stream: {}".format(stream_name))
            s = stream(client, config)
            singer.write_schema(s.name, s.load_schema(), s.key_properties)
            s.sync(state)
    LOGGER.info("Finished sync")
