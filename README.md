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

Log-enricher runs Enrichers, and is configured with a simple dictionary:

```python
from log_enricher import initialize_logging

from log_enricher.enrichers import Enricher

class RequestIDEnricher(Enricher):
    def __call__(self) -> Dict[str, Any]:
        return {"request_id": get_request_id()}

config = {
    "handlers": "plain"/"structured",
    "log_level": "DEBUG",
    "app_version": "xyz",
    "release_stage": "staging",
    "loggers": ["py", "mylogger"]
}

initialize_logging(config, enrichers=[RequestIDEnricher()])
```

Logs will be output in a plain, console-friendly format if `handlers` is 
`"plain"`, or in a structured JSON format if it is `"structured"`.

`initialize_logging()` will talk to and configure the `logging` subsystem. Once that has been called, `logging`
will use the new configuration.

options
-------
<!---
TODO: What options are allowed? What are they from?
-->

enrichers
---------
To build a log enricher, make a subclass of Enricher and implement `__call__()`. Any method returning a dict can 
be used to enrich log records, see [log_enricher/enrichers.py](log_enricher/enrichers.py).  The key-value pairs
in the dict are added as attribute-value pairs to the log record. Any method calls need to work in any subsequent
context the logging system is called.
