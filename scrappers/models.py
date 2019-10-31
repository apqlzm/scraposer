from dataclasses import dataclass
from typing import Optional


@dataclass
class SpotifyTrack:
    name: str
    artist: str
    uri: Optional[str] = None
