import logging
import logging.config
import sys

from typing import Any, Callable, Dict, List, Optional

from strenum import StrEnum
from sorcery import assigned_names

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


class Level(StrEnum):
    # Convenience enum that matches the logging library's levels
    # and autoconverts to a string to match initialize_logging(log_level)
    CRITICAL, FATAL, ERROR, WARNING, INFO, DEBUG = assigned_names()


def initialize_logging(
        loggers: List[str],
        structured_logs: bool = True,
        app_version: Optional[str] = None,
        release_stage: Optional[str] = None,
        log_level: Optional[str] = Level.INFO,
        enrichers: Optional[List[Callable]] = None
) -> None:
    """
    Sets up the python `logging` module by calling logging.config.dictConfig:
    https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig
    Python `logging` config dict schema: https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    Args:
        loggers: The loggers to be configured, e.g. ["py", "mylogger"]
        structured_logs: Whether logs should be structured ('structured' vs. 'plain' in 'handlers')
        app_version: The version of the running app
        release_stage: Where the app is running, e.g. "staging" or "production"
        log_level: Log severity level
        enrichers: A list of callable enricher classes
    """
    log_mode = "structured" if structured_logs else "plain"
    if app_version is None:
        app_version = "N/A"
    if release_stage is None:
        release_stage = "unknown"
    logging_config = make_config(app_version, release_stage, enrichers)
    for logger in loggers:
        logging_config["loggers"][logger] = {"handlers": [log_mode], "level": log_level, "propagate": False}
    logging.config.dictConfig(logging_config)
    logging.captureWarnings(True)
