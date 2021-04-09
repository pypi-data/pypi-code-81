import datetime

from rollbot_crawlab.db.mongo import get_col


def get_source(url):
    block = None
    col = get_col("sources")
    source = col.find_one({"url": url})
    if source is None \
            or 'enabled' not in source \
            or source['enabled'] is False \
            or 'block_id' not in source \
            or 'url' not in source \
            or 'identification' not in source:
        return None, None
    block_id = source.get("block_id")
    if block_id:
        block_col = get_col("blocks")
        block = block_col.find_one({"identification": block_id})
    if block is None:
        return None, None
    source["total_count"] = get_source_total(source)
    return source, block


def update_source_begin(source):
    col = get_col("sources")
    col.update_one({"_id": source["_id"]}, {"$set": {"latest_start_at": datetime.datetime.now()}})


def update_source_error(source, err_msg):
    col = get_col("sources")
    col.update_one({"_id": source["_id"]}, {"$set": {"err_msg": err_msg}})


def get_source_total(source):
    col = get_col()
    where = {"source_id": source["identification"]}
    return col.count(where)


def update_source_latest(source, latest_url, latest_count):
    col = get_col("sources")
    total_count = source.get("total_count", 0)
    where = {"_id": source["_id"]}

    json_obj = {
        "latest_count": latest_count,
        "latest_end_at": datetime.datetime.now(),
        "total_count": (total_count + latest_count)
    }

    if latest_url:
        json_obj["latest_url"] = latest_url

    update = {
        "$set": json_obj
    }
    col.update_one(where, update)
