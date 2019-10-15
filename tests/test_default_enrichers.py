import pytest
import platform
import threading
import datetime

from freezegun import freeze_time

from log_enricher import ContextFilter, default_enrichers


@pytest.fixture
def config():
    return dict(
        app_version="very.mock",
        release_stage="mockduction",
    )


class Record:
    name = "mock"
    levelname = "info"


@pytest.fixture
def context_filter(config):
    return ContextFilter(enrichers=default_enrichers(config))


def test_context_filter_adds_app_version(context_filter, config):
    record = Record()
    context_filter.filter(record)
    assert record.app_version == config['app_version']


def test_context_filter_adds_release_stage(context_filter, config):
    record = Record()
    context_filter.filter(record)
    assert record.release_stage == config['release_stage']


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
