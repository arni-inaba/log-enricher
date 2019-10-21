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

The log-enricher takes in a list of functions that return a dictionary:
```python
import os

from log_enricher import initialize_logging, Level
from app import current_user_context

def main():
    extra_log_properties = {
        "app_version": os.environ.get("APP_VERSION", "N/A"),
        "release_stage": os.environ.get("RELEASE_STAGE", "unknown"),
    }
    initialize_logging(
        loggers=["uvicorn", "sqlalchemy"],
        structured_logs=os.environ.get("STRUCTURED_LOGS", True),
        log_level=Level.INFO,
        enrichers=[current_user_context, lambda: extra_log_properties],
    )
```
Logs will be output in a structured JSON format if `structured_logs` is `True`,
or in a plain, console-friendly format if it is `False`.

enrichers
---------
To build a log enricher, make a subclass of Enricher and implement `__call__()`. Any method returning a dict can 
be used to enrich log records, see [log_enricher/enrichers.py](log_enricher/enrichers.py).  The key-value pairs
in the dict are added as attribute-value pairs to the log record. Any method calls need to work in any subsequent
context the logging system is called.