import logging
import logging.config
import sys

from typing import Any, Callable, Dict, List, Optional

from .enrichers import Enricher, ConstantProperty, Host, Thread, Timestamp  # noqa: F401


class ContextFilter(logging.Filter):
    def __init__(self, enrichers: List[Callable] = None):
        super().__init__()
        if enrichers is None:
            enrichers = []
        self._enrichers = enrichers

    def filter(self, record):
        for enricher in self._enrichers:
            props = enricher()
            for attr, value in props.items():
                setattr(record, attr, value)

        # XXX: replace these with enrichers which take in record as an argument
        record.logger_name = record.name
        record.log_level = record.levelname
        return True


def default_enrichers(app_version: str, release_stage: str) -> List[Callable[[], Dict[str, Any]]]:
    return [
        ConstantProperty('app_version', app_version),
        ConstantProperty('release_stage', release_stage),
        Host(),
        Thread(),
        Timestamp(sep="T", timespec="milliseconds")
    ]


def make_config(
        app_version: str,
        release_stage: str,
        enrichers: Optional[List[Callable[[], Dict[str, Any]]]] = None
) -> Dict:
    if enrichers is None:
        enrichers = []

    return {
        "version": 1,
        "formatters": {
            "json": {"class": "pythonjsonlogger.jsonlogger.JsonFormatter"},
            "plain": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "filters": {
            "context": {
                "()": "log_enricher.ContextFilter",
                "enrichers": default_enrichers(app_version, release_stage) + enrichers,
            }
        },
        "handlers": {
            "structured": {"class": "logging.StreamHandler", "formatter": "json", "filters": ["context"]},
            "plain": {"class": "logging.StreamHandler", "formatter": "plain", "filters": ["context"]},
        },
        "stream": sys.stdout,
        "loggers": {},
    }


def initialize_logging(
        log_mode: str,
        loggers: List[str],
        app_version: Optional[str],
        release_stage: Optional[str],
        log_level: Optional[str] = "INFO",
        enrichers: Optional[List[Callable]] = None
) -> None:
    """
    Sets up the python `logging` module by calling logging.config.dictConfig:
    https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig
    Python `logging` config dict schema: https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    config = {
        "log_mode": "plain"/"structured",
        "log_level": "DEBUG",
        "app_version": "xyz",
        "release_stage": "staging",
        "loggers": ["py", "mylogger"]
    }
    Args:
        log_mode: Either "structured" or "plain"
        loggers: The loggers to be configured
        app_version: The version of the running app
        release_stage: Where the app is running, e.g. "staging" or "production"
        log_level: Log severity level
        enrichers: A list of callable enricher classes
    """
    if app_version is None:
        app_version = "N/A"
    if release_stage is None:
        release_stage = "unknown"
    logging_config = make_config(app_version, release_stage, enrichers)
    for logger in loggers:
        logging_config["loggers"][logger] = {"handlers": [log_mode], "level": log_level, "propagate": False}
    logging.config.dictConfig(logging_config)
    logging.captureWarnings(True)
