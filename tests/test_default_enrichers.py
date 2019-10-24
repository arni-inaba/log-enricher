import pytest
import platform
import threading
import datetime

from freezegun import freeze_time

from log_enricher import ContextFilter, default_enrichers


class Record:
    name = "mock"
    levelname = "info"


@pytest.fixture
def context_filter():
    return ContextFilter(enrichers=default_enrichers())


def test_context_filter_adds_host(context_filter):
    record = Record()
    context_filter.filter(record)
    assert record.host == platform.node()


def test_context_filter_adds_thread_id(context_filter):
    record = Record()
    context_filter.filter(record)
    assert record.thread_id == threading.current_thread().getName()


@freeze_time()
def test_context_filter_adds_timestamp(context_filter):
    record = Record()
    context_filter.filter(record)
    assert record.timestamp == datetime.datetime.now().isoformat(sep="T", timespec="milliseconds")
