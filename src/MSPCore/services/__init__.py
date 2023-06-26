from __future__ import annotations
from abc import ABC, abstractmethod
import logging
from typing import Any, TYPE_CHECKING

from mspcore import downloader

from mspcore import errors

if TYPE_CHECKING:
    from mspcore import MSPCore
    from mspcore.player.track import Track


class Service(ABC):
    name: str
    is_enabled: bool
    hidden: bool
    hostnames: list[str]
    error_message: str
    warning_message: str
    help: str

    def download(self, track: Track, file_path: str) -> None:
        downloader.download_file(track.url, file_path)

    @abstractmethod
    def get(
        self,
        url: str,
        extra_info: dict[str, Any] | None = None,
        process: bool = False,
    ) -> list[Track]:
        ...

    @abstractmethod
    def initialize(self) -> None:
        ...

    @abstractmethod
    def search(self, query: str) -> list[Track]:
        ...


from mspcore.services.vk import VkService
from mspcore.services.yam import YamService
from mspcore.services.yt import YtService


class ServiceManager:
    __instance = None

    def __init__(self, core: MSPCore) -> None:
        if self.__instance:
            raise RuntimeError("Cann't create this object twice")
        ServiceManager.__instance = self
        self.config = core.config.services
        self.services: dict[str, Service] = {
            "vk": VkService(core, self.config.vk),
            "yam": YamService(core, self.config.yam),
            "yt": YtService(core, self.config.yt),
        }
        self.service: Service = self.services[self.config.default_service]
        self.fallback_service = self.config.fallback_service

    def initialize(self) -> None:
        logging.debug("Initializing services")
        for service in self.services.values():
            if not service.is_enabled:
                continue
            try:
                service.initialize()
            except errors.ServiceError as e:
                service.is_enabled = False
                service.error_message = str(e)
                if self.service == service:
                    self.service = self.services[self.fallback_service]
        logging.debug("Services initialized")

    @classmethod
    def get_service_by_name(cls, name: str) -> Service:
        if not cls.__instance:
            raise RuntimeError("Has not been created")
        try:
            service = cls.__instance.services[name]
            if not service.is_enabled:
                raise errors.ServiceIsDisabledError(service.error_message)
            return service
        except KeyError as e:
            raise errors.ServiceNotFoundError(str(e))
