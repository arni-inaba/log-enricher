import platform
import threading

import pytest

from log_enricher import ContextFilter
from log_enricher.enrichers import Host, Thread, ProcessID
from tests.utils.utils import Record


@pytest.fixture
def context_filter():
    return ContextFilter(enrichers=[Host(), Thread(), ProcessID()])


def test_context_filter_adds_host(context_filter):
    record = Record()
    context_filter.filter(record)
    assert record.host == platform.node()


def test_context_filter_adds_thread_id(context_filter):
    record = Record()
    context_filter.filter(record)
    assert record.thread_id == threading.current_thread().getName()


def test_context_filter_adds_process_id(context_filter):
    record = Record()
    context_filter.filter(record)
    assert isinstance(record.process_id, int)
