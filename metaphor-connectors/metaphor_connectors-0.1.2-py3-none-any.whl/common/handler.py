import json
import logging
from typing import Type

from smart_open import open

from metaphor.common.extractor import BaseExtractor, RunConfig

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle_api(
    event, context, runConfig: Type[RunConfig], extractor: Type[BaseExtractor]
):
    try:
        return _handle_api(event, context, runConfig, extractor)
    except Exception as e:
        logger.exception(str(e))
        return {"statusCode": 500, "body": str(e)}


def _handle_api(
    event, context, runConfig: Type[RunConfig], extractor: Type[BaseExtractor]
):
    params = json.loads(event["body"]) if "body" in event else event["params"]
    config_file = params.get("config_file", None)
    if config_file is None:
        return {"statusCode": 422, "body": f"Missing 'config_file' parameter"}

    with open(config_file, encoding="utf8") as fin:
        config_dict = json.load(fin)

    for key in runConfig.parameters():
        if key not in config_dict:
            return {"statusCode": 422, "body": f"Missing '{key}' key in {config_file}"}

    actor = extractor()
    actor.run(config=runConfig.build(config_dict))
    return {"statusCode": 200, "body": json.dumps(params)}
