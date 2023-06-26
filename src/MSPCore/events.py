import logging
from typing import Callable, Generic, TypeVarTuple, Unpack

from mspcore.player.enums import State
from mspcore.player.track import Track


T = TypeVarTuple("T")


class EventHandler(Generic[*T]):
    def __init__(self):
        self.callbacks: set[Callable[[Unpack[T]], None]] = set()

    def __call__(self, *args: Unpack[T]) -> None:
        for callback in self.callbacks:
            try:
                callback(*args)
            except Exception as e:
                logging.error(f"Error {e} while calling callback")

    def register(self, callback: Callable[[Unpack[T]], None]):
        self.callbacks.add(callback)

    def unregister(self, callback: Callable[[Unpack[T]], None]):
        self.callbacks.remove(callback)


class Events:
    def __init__(self):
        self.player_state_update = EventHandler[State]()
        self.player_track_update = EventHandler[Track]()
