from typing import List, Optional, Union

from .account.status import Status
from .album.album import Album
from .artist.artist_tracks import ArtistTracks
from .playlist.playlist import Playlist
from .search.search import Search
from .track.track import Track
from .utils.request import Request

class Client:
    def __init__(
        self,
        token: Optional[str] = ...,
        base_url: Optional[str] = ...,
        request: Optional[Request] = ...,
        language: str = ...,
        report_unknown_fields: bool = ...,
    ) -> None: ...
    def account_status(
        self, timeout: Optional[Union[int, float]] = ...
    ) -> Optional[Status]: ...
    def albums_with_tracks(
        self, album_id: Union[str, int], timeout: Optional[Union[int, float]] = ...
    ) -> Optional[Album]: ...
    def artists_tracks(
        self,
        artist_id: Union[str, int],
        page: int = ...,
        page_size: int = ...,
        timeout: Optional[Union[int, float]] = ...,
    ) -> ArtistTracks: ...
    def init(self) -> None: ...
    def tracks(
        self,
        track_ids: Union[List[Union[str, int]], int, str],
        with_positions: bool = ...,
        timeout: Optional[Union[int, float]] = ...,
    ) -> List[Track]: ...
    def search(
        self,
        text: str,
        nocorrect: bool = ...,
        type_: str = ...,
        page: int = ...,
        playlist_in_best: bool = ...,
        timeout: Optional[Union[int, float]] = ...,
    ) -> Optional[Search]: ...
    def users_playlists(
        self,
        kind: Union[List[Union[str, int]], str, int],
        user_id: Optional[Union[str, int]] = ...,
        timeout: Optional[Union[int, float]] = ...,
    ) -> Union[Playlist, List[Playlist]]: ...
