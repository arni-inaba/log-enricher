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

`log-enricher.initialize_logging(...)` configures the `logging` library and takes in `enrichers`, a list of 
functions that return a dictionary. When a log message is sent, the enrichers are run automatically and their 
output is added to the log message, if structured logging is enabled.

Furthermore, `initialize_logging()` takes a list of `loggers` to use, a switch to control `structured_logs` 
(JSON logs, default on), and a `log_level` setting.

Logs will be output in a structured JSON format by default - if `structured_logs` is `True` - 
or in a plain, console-friendly format if `structured_logs` is `False`.

config example
--------------
```python
import os

from log_enricher import initialize_logging, Level
from log_enricher.enrichers import Enricher

class UserContextEnricher(Enricher):
    def __call__(self) -> Dict[str, Any]:
        user_context = get_user_context()
        return {"username": user_context.get("username")}

extra_log_properties = {
    "app_version": Config.APP_VERSION, "release_stage": Config.RELEASE_STAGE
}

def main():
    initialize_logging(
        loggers=["uvicorn", "sqlalchemy"],
        structured_logs=os.environ.get("STRUCTURED_LOGS", True),
        log_level=Level.INFO,
        enrichers=[UserContextEnricher(), lambda: extra_log_properties],
    )
```

enrichers
---------
To build a log enricher, make a subclass of Enricher, or Callable, and implement `__call__()`. Any method returning 
a dict can be used to enrich log records. See [log_enricher/enrichers.py](log_enricher/enrichers.py). The key-value
pairs in the dict are added as attribute-value pairs to the log record. Of course, any method calls in the 
enrichers need to  work in any subsequent context the logging system is called.
