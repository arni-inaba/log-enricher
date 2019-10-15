import datetime
import logging
import logging.config
import platform
import sys
import threading

from typing import Callable, Dict, List

from .enrichers import Enricher, ConfigProperty, Host, Thread, Timestamp


class ContextFilter(logging.Filter):
    def __init__(self, request_id_getter: Callable, user_context_getter: Callable, enrichers: List[Enricher] = None):
        super().__init__()
        if enrichers is None:
            enrichers = []
        self._enrichers = enrichers

        self.request_id_getter = request_id_getter
        self.user_context_getter = user_context_getter

    def filter(self, record):
        for enricher in self._enrichers:
            props = enricher()
            for attr, value in props.items():
                setattr(record, attr, value)

        if self.request_id_getter:
            request_id = self.request_id_getter()
            if request_id:
                record.request_id = request_id
        if self.user_context_getter:
            user_context = self.user_context_getter()
            if user_context:
                record.username = user_context.get("username")
                record.user_id = user_context.get("user_id")
                record.path = user_context.get("path")
        record.logger_name = record.name
        record.log_level = record.levelname
        return True


def default_enrichers(config: Dict) -> List[Enricher]:
    return [
        ConfigProperty(config, 'app_version'),
        ConfigProperty(config, 'release_stage'),
        Host(),
        Thread(),
        Timestamp(sep="T", timespec="milliseconds")
    ]


def initialize_logging(config: Dict, request_id_getter: Callable, user_context_getter: Callable) -> None:
    handlers = ["plain"] if config.get("log_mode") == "PLAIN" else ["structured"]
    log_level = config.get("log_level", "INFO")
    logging_config = {
        "version": 1,
        "formatters": {
            "json": {"class": "pythonjsonlogger.jsonlogger.JsonFormatter"},
            "plain": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "filters": {
            "context": {
                "()": "log_enricher.ContextFilter",
                "request_id_getter": request_id_getter,
                "user_context_getter": user_context_getter,
                "enrichers": default_enrichers(config),
            }
        },
        "handlers": {
            "structured": {"class": "logging.StreamHandler", "formatter": "json", "filters": ["context"]},
            "plain": {"class": "logging.StreamHandler", "formatter": "plain", "filters": ["context"]},
        },
        "stream": sys.stdout,
        "loggers": {},
    }
    for logger in config.get("loggers"):
        logging_config["loggers"][logger] = {"handlers": handlers, "level": log_level, "propagate": False}
    logging.config.dictConfig(logging_config)
    logging.captureWarnings(True)
