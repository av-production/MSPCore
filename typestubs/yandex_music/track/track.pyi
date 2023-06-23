from typing import List, Optional

from ..download_info import DownloadInfo
from ..artist.artist import Artist


class Track:
    artists: Optional[List[Artist]]
    def get_download_info(self, get_direct_links: bool = ...) -> List[DownloadInfo]: ...

    title: str
    track_id: str
