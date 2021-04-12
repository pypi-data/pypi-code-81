from singer.catalog import Catalog, CatalogEntry, Schema

from streams import STREAMS


def discover():
    catalog = Catalog([])

    for stream_name in STREAMS:
        stream = STREAMS[stream_name]
        s = stream()
        catalog.streams.append(
            CatalogEntry(
                stream=stream_name,
                tap_stream_id=stream_name,
                schema=Schema.from_dict(s.load_schema()),
                metadata=s.load_metadata(),
                table=stream_name,
                replication_key=s.replication_key,
                replication_method=s.replication_method,
            )
        )

    return catalog
