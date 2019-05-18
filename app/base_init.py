import logging
import argparse
import os
import json


def init_log(level=logging.INFO,
             filename=None,
             format="[%(asctime)s] %(levelname).1s %(message)s",
             datefmt="%Y.%m.%d %H:%M:%S"
             ):
    logging.basicConfig(format=format, datefmt=datefmt, level=level, filename=filename)


def get_config_path():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default="config.json", help="config file")
    namespace = parser.parse_args()
    return namespace.config


def load_config(config, filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError("config file not found")
    with open(filepath) as f:
        conf_from_file = json.load(f)
        if not isinstance(conf_from_file, dict):
            raise TypeError("Wrong data format in config file")
        for key, value in conf_from_file.items():
            config[key] = value

    if "LOGGING_LEVEL" not in config:
        config["LOGGING_LEVEL"] = logging.INFO

    if "LOGGING_FILE" not in config:
        config["LOGGING_FILE"] = "log.log"


def init(config=None):
    if config is None:
        config = {}
    load_config(config, get_config_path())
    init_log(config["LOGGING_LEVEL"], config["LOGGING_FILE"])
    return config
