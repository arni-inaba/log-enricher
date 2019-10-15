import datetime
import logging
import logging.config
import platform
import sys
import threading


class ContextFilter(logging.Filter):
    def __init__(self, config, request_id_getter, user_context_getter):
        super().__init__()
        self.config = config
        self.request_id_getter = request_id_getter
        self.user_context_getter = user_context_getter

    def filter(self, record):
        record.app_version = self.config.APP_VERSION
        record.release_stage = self.config.RELEASE_STAGE
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
    handlers = ["plain"] if config.LOG_MODE == "PLAIN" else ["structured"]
    log_level = "DEBUG" if config.DEBUG else "INFO"
    logging_config = {
        "version": 1,
        "formatters": {
            "json": {"class": "pythonjsonlogger.jsonlogger.JsonFormatter"},
            "plain": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "filters": {
            "context": {
                "()": "log_enricher.ContextFilter",
                "config": config,
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
    for logger in config.LOGGERS:
        logging_config["loggers"][logger] = {"handlers": handlers, "level": log_level, "propagate": False}
    logging.config.dictConfig(logging_config)
    logging.captureWarnings(True)
