import logging
import logging.config
import sys

from typing import Any, Callable, Dict, List, Optional

from strenum import StrEnum  # type: ignore

from .enrichers import Enricher, ConstantProperty, Timestamp  # noqa: F401


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


def default_enrichers() -> List[Callable[[], Dict[str, Any]]]:
    return [Timestamp(sep="T", timespec="milliseconds")]


def make_config(enrichers: Optional[List[Callable[[], Dict[str, Any]]]] = None) -> Dict:
    if enrichers is None:
        enrichers = []

    return {
        "version": 1,
        "formatters": {
            "json": {"class": "pythonjsonlogger.jsonlogger.JsonFormatter"},
            "plain": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "filters": {"context": {"()": "log_enricher.ContextFilter", "enrichers": default_enrichers() + enrichers}},
        "handlers": {
            "structured": {"class": "logging.StreamHandler", "formatter": "json", "filters": ["context"]},
            "plain": {"class": "logging.StreamHandler", "formatter": "plain", "filters": ["context"]},
        },
        "stream": sys.stdout,
        "loggers": {},
    }


class Level(StrEnum):
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


def configure_loggers(loggers, complex_loggers, log_mode, log_level):
    if loggers is None:
        loggers = []
    if complex_loggers is None:
        complex_loggers = []
    loggers_cfg = {}
    for logger in loggers:
        loggers_cfg[logger] = {"handlers": [log_mode], "level": log_level, "propagate": True}
    for logger in complex_loggers:
        loggers_cfg[logger["name"]] = {
            "handlers": [log_mode],
            "level": logger["log_level"],
            "propagate": True,
        }
    return loggers_cfg


def initialize_logging(
    loggers: Optional[List[str]] = None,
    complex_loggers: Optional[List[dict]] = None,
    structured_logs: bool = True,
    log_level: Optional[str] = Level.INFO,
    enrichers: Optional[List[Callable]] = None,
) -> None:
    """
    Sets up the python `logging` module by calling logging.config.dictConfig:
    https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig
    Python `logging` config dict schema: https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    Args:
        loggers: The loggers to be configured, e.g. ["py", "mylogger"]
        complex_loggers: Loggers that need a specific log level
        structured_logs: Whether logs should be structured ('structured' vs. 'plain' in 'handlers')
        log_level: Log severity level
        enrichers: A list of callable enricher classes
    """
    log_mode = "structured" if structured_logs else "plain"
    logging_config = make_config(enrichers)
    logging_config["loggers"] = configure_loggers(loggers, complex_loggers, log_mode, log_level)
    logging.config.dictConfig(logging_config)
    logging.captureWarnings(True)
