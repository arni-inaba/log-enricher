log-enricher
============
[![CircleCI](https://circleci.com/gh/arni-inaba/log-enricher.svg?style=svg)](https://circleci.com/gh/arni-inaba/log-enricher)
[![PyPI Downloads](https://img.shields.io/pypi/dm/log-enricher.svg)](https://pypi.org/project/log-enricher/)
[![PyPI Version](https://img.shields.io/pypi/v/log-enricher.svg)](https://pypi.org/project/log-enricher/)
[![License](https://img.shields.io/badge/license-mit-blue.svg)](https://pypi.org/project/log-enricher/)

This is a log enricher, useful for adding custom fields to log records.

This was developed at [GRID](https://github.com/GRID-is) for use with our
python backend services and intended to emit structured logs.

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
    "handlers": "plain"/"structured",
    "log_level": "DEBUG",
    "app_version": "xyz",
    "release_stage": "staging",
    "loggers": ["py", "mylogger"]
}
```
Logs will be output in a plain, console-friendly format if `handlers` is 
`"plain"`, or in a structured JSON format if it is `"structured"`.