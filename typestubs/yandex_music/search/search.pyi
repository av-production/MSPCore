from typing import Optional

from .search_result import SearchResult
from ..track.track import Track

class Search:
    podcast_episodes: Optional[SearchResult[Track]]
    tracks: Optional[SearchResult[Track]]
