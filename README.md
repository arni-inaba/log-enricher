log-enricher
============

This is a log enricher, useful for adding custom fields to log records

installation
------------
```
pip install log-enricher
```

configuration
-------------

The log-enricher is configured with a simple dictionary:
```
config = {
    "log_mode": "PLAIN",
    "log_level": "DEBUG",
    "app_version": "xyz",
    "release_stage": "staging"
    "loggers": ["py", "mylogger"],
}
```
Logs will be output in a plain, console-friendly format if log_mode is `PLAIN`,
otherwise they will be in a structured JSON format.