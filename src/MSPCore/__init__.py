import logging
import sys
from typing import Any

from MSPCore import (
    config,
    events,
    player,
    services,
    url_handler,
)

from pydantic.error_wrappers import ValidationError


class MSPCore:
    def __init__(
        self,
        config_data: dict[Any, Any] = {},
        logger: logging.Logger = logging.root,
    ) -> None:
        try:
            self.config = config.ConfigModel(**config_data)
        except ValidationError as e:
            for error in e.errors():
                print(
                    "Error in config:",
                    ".".join([str(i) for i in error["loc"]]),
                    error["msg"],
                )
            sys.exit(1)
        self.events = events.Events()
        self.player = player.Player(self)
        self.service_manager = services.ServiceManager(self)
        self.url_handler = url_handler.UrlHandler(self)

    def initialize(self):
        logging.debug("Initializing")
        self.player.initialize()
        self.service_manager.initialize()
        logging.debug("Initialized")

    def run(self):
        logging.debug("Starting")
        self.player.run()
        logging.info("Started")

    def close(self) -> None:
        logging.debug("Closing MSPCore")
        self.player.close()
        logging.info("MSPCore closed")
