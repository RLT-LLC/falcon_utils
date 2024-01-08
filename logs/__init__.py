import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os
from pathlib import Path


def _ensure_logs_folder_exists():
    logs_folder = Path(os.getcwd()).joinpath('logs')
    if not logs_folder.exists():
        os.mkdir(logs_folder)
    return logs_folder


def declare_logger(service_name):
    _ensure_logs_folder_exists()
    formatter = logging.Formatter("%(asctime)s | %(message)s", datefmt='%m/%d/%Y %H:%M:%S')
    handler = RotatingFileHandler(F'./logs/{service_name}_{datetime.now().strftime("%d.%m.%Y")}.log',
                                  maxBytes=204800, encoding="utf-8")
    handler.setFormatter(formatter)
    logger = logging.getLogger(service_name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
