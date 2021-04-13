import os
from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML(typ="safe")
POSTGRES_ENVIRONMENT_VARIABLES = {
    "POSTGRES_HOST",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "PGDB",
}


def prepare_for_store_test(source_path, target_path):
    conf = yaml.load(Path(source_path))
    rewrite_config = all(
        k in os.environ for k in POSTGRES_ENVIRONMENT_VARIABLES
    )
    if rewrite_config:
        conf["store_uri"] = "postgres://%s:%s@%s/%s" % (
            os.environ["POSTGRES_USER"],
            os.environ["POSTGRES_PASSWORD"],
            os.environ["POSTGRES_HOST"],
            os.environ["PGDB"],
        )
        conf["logging"]["loggers"]["palaestrai.store"]["level"] = "DEBUG"
    with open(target_path, "w") as fp:
        yaml.dump(conf, fp)
