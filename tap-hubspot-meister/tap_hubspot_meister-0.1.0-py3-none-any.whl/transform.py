import singer
from singer import Transformer, metadata, utils

LOGGER = singer.get_logger()


def transform_and_log(self, state, record, mdate, current_bookmark):
    time_extracted = utils.now()
    transformer = Transformer()
    outcome = False
    try:
        record = transformer.transform(
            record, self.load_schema(), metadata.to_map(self.load_metadata())
        )
        if utils.strptime_with_tz(record[mdate]) >= current_bookmark:
            self.update_bookmark(state, record[mdate])
        outcome = True
    except Exception as err:
        LOGGER.error("Transformer Error: {}".format(err))
        raise err
    try:
        singer.write_record(self.name, record, time_extracted=time_extracted)
    except OSError as err:
        LOGGER.error("OS Error writing record for: {}".format(self.name))
        LOGGER.error("Stream: {}, record: {}".format(self.name, record))
        raise err
    except TypeError as err:
        LOGGER.error("Type Error writing record for: {}".format(self.name))
        LOGGER.error("Stream: {}, record: {}".format(self.name, record))
        raise err
    return outcome
