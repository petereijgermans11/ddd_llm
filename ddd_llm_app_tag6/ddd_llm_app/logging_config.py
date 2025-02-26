import logging
import os
import sys

import logging.config

import yaml
from omegaconf import OmegaConf
from typing_extensions import deprecated

from ddd_llm_app.config import Config

@deprecated("Use setup_logger2 instead")
def setup_logger(config_log_level: str = None):
    """
    Set up the application logger.
    Logs to console and optionally to a file.
    """

    if config_log_level:
        log_level = getattr(logging, config_log_level.upper() )
    else:
        log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)


    # Define the log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    logger.info(f"Log level set to: {log_level}")
    print(f"Log level set to: {log_level}")

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (only in standalone mode)
    if not os.getenv("RUNNING_IN_CONTAINER"):
        file_handler = logging.FileHandler(Config.config['logging']['logfile'])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def _load_yaml_config(config_file: str)-> dict:
    with open(config_file, "r") as file:
        return yaml.safe_load(file)


def setup_logger2(config_log_level: str = None):
    # config = _load_yaml_config()
    logging.config.dictConfig(OmegaConf.to_container( Config.config['logging']))
    if config_log_level:
        log_level = getattr(logging, config_log_level.upper() )
    else:
        log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)
    logging.root.setLevel(log_level)
    logger = logging.getLogger(__name__)
    logger.info(f"Root Log level set to: {logging.getLevelName(log_level)}")


