import datetime

import pytest
from freezegun import freeze_time

from log_enricher import ContextFilter, default_enrichers


class Record:
    name = "mock"
    levelname = "info"


@pytest.fixture
def context_filter():
    return ContextFilter(enrichers=default_enrichers())


@freeze_time()
def test_context_filter_adds_timestamp(context_filter):
    record = Record()
    context_filter.filter(record)
    assert record.timestamp == datetime.datetime.now().isoformat(sep="T", timespec="milliseconds")
