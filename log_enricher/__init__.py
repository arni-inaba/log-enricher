import datetime
import logging
import logging.config
import platform
import sys
import threading

from typing import Dict, Any


class Enricher(ABC):
    @abstractmethod
    def get(self) -> Dict[str, Any]:
        raise NotImplementedError


class AppVersion(Enricher):
    def __init__(self, app_version: str):
        self.app_version = app_version

    def get(self) -> Dict[str, Any]:
        return {'app_version': self.app_version}


class ReleaseStage(Enricher):
    def __init__(self, release_stage: str):
        self.release_stage = release_stage

    def get(self) -> Dict[str, Any]:
        return {'release_stage': self.release_stage}


class ContextFilter(logging.Filter):
    def __init__(self, enrichers: List[Enricher]):
        super().__init__()
        self._enrichers = enrichers

        self.request_id_getter = request_id_getter
        self.user_context_getter = user_context_getter

    def filter(self, record):
        for enricher in self._enrichers:
            props = enricher.get()
            for attr, value in props.items():
                setattr(record, attr, value)

        record.host = platform.node()
        record.thread_id = threading.current_thread().getName()
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
        record.timestamp = datetime.datetime.now().isoformat(sep="T", timespec="milliseconds")
        record.logger_name = record.name
        record.log_level = record.levelname
        return True


def initialize_logging(config, request_id_getter, user_context_getter) -> None:
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
                "enrichers": [AppVersion(config.APP_VERSION), ReleaseStage(config.RELEASE_STAGE)]
                "request_id_getter": request_id_getter,
                "user_context_getter": user_context_getter,
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
