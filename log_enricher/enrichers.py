import datetime
import platform
import threading

from abc import ABC, abstractmethod

from typing import Dict, Any


class Enricher(ABC):
    @abstractmethod
    def get(self) -> Dict[str, Any]:
        raise NotImplementedError


class AppVersion(Enricher):
    def __init__(self, app_version: str):
        self.app_version = app_version

    def get(self) -> Dict[str, Any]:
        return {'app_version': self.app_version}


class ReleaseStage(Enricher):
    def __init__(self, release_stage: str):
        self.release_stage = release_stage

    def get(self) -> Dict[str, Any]:
        return {'release_stage': self.release_stage}


class Host(Enricher):
    def get(self) -> Dict[str, Any]:
        return {'host': platform.node()}


class Thread(Enricher):
    def get(self) -> Dict[str, Any]:
        return {'thread_id': threading.current_thread().getName()}


class Timestamp(Enricher):
    """ Timestamp enrichers, adds an ISO-8601 timestamp to a log record with the attribute name 'timestamp'

    Parameters:
    **kwargs (dict): keyword arguments passed into datetime.isoformat(**kwargs)
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get(self) -> Dict[str, Any]:
        return {'timestamp': datetime.datetime.now().isoformat(**self.kwargs)}
