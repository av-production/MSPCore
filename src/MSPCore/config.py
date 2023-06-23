from typing import Any

from pydantic import BaseModel


class PlayerModel(BaseModel):
    default_volume: int = 50
    max_volume: int = 100
    volume_fading: bool = True
    volume_fading_interval: float = 0.025
    seek_step: int = 5
    player_options: dict[str, Any] = {}


class VkModel(BaseModel):
    enabled: bool = True
    token: str = ""


class YtModel(BaseModel):
    enabled: bool = True


class YamModel(BaseModel):
    enabled: bool = True
    token: str = ""


class ServicesModel(BaseModel):
    default_service: str = "vk"
    fallback_service: str = "yt"
    vk: VkModel = VkModel()
    yam: YamModel = YamModel()
    yt: YtModel = YtModel()


class ConfigModel(BaseModel):
    player: PlayerModel = PlayerModel()
    services: ServicesModel = ServicesModel()
