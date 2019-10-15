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
    def get(self) -> Dict[str, Any]:
        return {'timestamp': datetime.datetime.now().isoformat(sep="T", timespec="milliseconds")}
