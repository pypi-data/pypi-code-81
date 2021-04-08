import json
from datetime import date, time, datetime
from pathlib import Path
from typing import Any, Tuple


def read_json_dict_from_file(path: Path) -> dict:
    with open(path, mode='r', newline=None) as json_file:
        json_inst = json.load(json_file)
    return json_inst


# TODO need to pull out values from specific models
# models has array of model dicts
# model has values
# one value is the model id: ID
# others are the values such as WH
def get_model_value(model_id: int, value_id: str, reading: dict) -> Any:
    models = reading["models"]
    model = next(item for item in models if item["ID"] == model_id)
    return model[value_id]


def get_reading_date(reading: dict) -> Tuple[date, time]:
    date_string = reading.get("reading_date")
    date_time = datetime.fromisoformat(date_string)
    return date_time.date(), date_time.time()
