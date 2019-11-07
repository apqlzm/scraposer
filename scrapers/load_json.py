"""
Load json with following structure:
[
        
    {
        "artist": "NZCA Lines",
        "title": "Persephone Dreams"
    },
    {
        "artist": "Boikafe",
        "title": "Studio 9 Tool"
    }
    ...
]

Json can be obtained from 
Akademickie Radio Luz http://radioluz.pwr.edu.pl/playlista/

"""

import json
from typing import List

from scrapers.models import SpotifyTrack


def __load_json(file_path) -> List[dict]:
    with open(file_path, mode="r") as f:
        data = json.load(f)
        return data


def __prepare_list_of_tracks(obj_list: List[dict]):
    tracks = []
    for item in obj_list:
        artist = item["artist"]
        track_name = item["title"]
        tracks.append(SpotifyTrack(name=track_name, artist=artist))
    return tracks


def tracks(file_path: str):
    r = __load_json(file_path)
    tracks = __prepare_list_of_tracks(r)
    return tracks


if __name__ == "__main__":
    r = __load_json("/tmp/aaa.json")
    tracks = __prepare_list_of_tracks(r)
    print(tracks)
