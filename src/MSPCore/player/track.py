from __future__ import annotations

import os
from threading import Lock
from typing import Any, TYPE_CHECKING

from MSPCore import utils
from MSPCore.player.enums import TrackType

if TYPE_CHECKING:
    from MSPCore.services import Service


class Track:
    format: str
    type: TrackType

    def __init__(
        self,
        service: Service = None,
        url: str = "",
        name: str = "",
        format: str = "",
        extra_info: dict[str, Any] | None = None,
        type: TrackType = TrackType.Default,
    ) -> None:
        self.service = service
        self.url = url
        self.name = name
        self.format = format
        self.extra_info = extra_info
        self.type = type
        self._lock = Lock()
        self._is_fetched = False

    def download(self, directory: str) -> str:
        file_name = self.name + "." + self.format
        file_name = utils.clean_file_name(file_name)
        file_path = os.path.join(directory, file_name)
        self.service.download(self, file_path)
        return file_path

    def _fetch_stream_data(self):
        if self.type != TrackType.Dynamic or self._is_fetched:
            return
        self._original_dict = self.get_dict()
        track = self.service.get(self._url, extra_info=self.extra_info, process=True)[0]
        self.url = track.url
        self.name = track.name
        self._original_dict["name"] = track.name
        self.format = track.format
        self.type = track.type
        self.extra_info = track.extra_info
        self._is_fetched = True

    @property
    def url(self) -> str:
        with self._lock:
            self._fetch_stream_data()
            return self._url

    @url.setter
    def url(self, value: str) -> None:
        self._url = value

    @property
    def name(self) -> str:
        with self._lock:
            if not self._name:
                self._fetch_stream_data()
            return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    def get_dict(self) -> dict[str, Any]:
        if hasattr(self, "_original_dict"):
            return self._original_dict
        return {
            "name": self._name,
            "url": self._url,
            "extra_info": self.extra_info,
            "service": self.service.name,
        }

    @staticmethod
    def from_dict(dict_: dict[str, Any]) -> Track:
        from MSPCore.services import ServiceManager

        return Track(
            name=dict_["name"],
            url=dict_["url"],
            extra_info=dict_["extra_info"],
            service=ServiceManager.get_service_by_name(dict_["service"]),
        )

    def __bool__(self):
        if self.service or self.url:
            return True
        return False
