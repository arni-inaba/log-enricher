import datetime
import os
import platform
import threading

from abc import ABC, abstractmethod

from typing import Dict, Any


class Enricher(ABC):
    @abstractmethod
    def __call__(self) -> Dict[str, Any]:
        raise NotImplementedError


class ConstantProperty(Enricher):
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def __call__(self) -> Dict[str, Any]:
        return {self.key: self.value}


class Host(Enricher):
    def __call__(self) -> Dict[str, Any]:
        return {'host': platform.node()}


class Thread(Enricher):
    def __call__(self) -> Dict[str, Any]:
        return {'thread_id': threading.current_thread().getName()}


class ProcessID(Enricher):
    def __call__(self) -> Dict[str, Any]:
        return {"process_id": os.getpid()}


class Timestamp(Enricher):
    """ Timestamp enrichers, adds an ISO-8601 timestamp to a log record with the attribute name 'timestamp'

    Parameters:
    **kwargs (dict): keyword arguments passed into datetime.isoformat(**kwargs)
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self) -> Dict[str, Any]:
        return {'timestamp': datetime.datetime.now().isoformat(**self.kwargs)}
