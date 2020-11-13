import datetime

import pytest
from freezegun import freeze_time

from log_enricher import ContextFilter, default_enrichers
from tests.utils.utils import Record


@pytest.fixture
def defaults_context_filter():
    return ContextFilter(enrichers=default_enrichers())


@freeze_time()
def test_context_filter_adds_timestamp(defaults_context_filter):
    record = Record()
    defaults_context_filter.filter(record)
    assert record.timestamp == datetime.datetime.now().isoformat(sep="T", timespec="milliseconds")
