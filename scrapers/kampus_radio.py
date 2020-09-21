"""Download playlist from Radio Kampus using it's api https://api.radiokampus.fm/playlista

"""

import re

import requests
from bs4 import BeautifulSoup

from scrapers.models import SpotifyTrack


def __download_json(url):
    headers = {
        "Origin": "https://radiokampus.fm",
        "Referer": "https://radiokampus.fm/playlista/",
    }
    result = requests.get(url, headers=headers)
    return result.json()


def __prepare_list_of_tracks(json_data):
    tracks = []
    for song_data in json_data:
        artist = song_data["artist"]
        track_name = song_data["title"]
        track_name = re.sub(r"\(feat.+\)", "", track_name)
        tracks.append(SpotifyTrack(name=track_name, artist=artist))
    return tracks


def tracks(url):
    """Downloads list of tracks
    Args:
        url: api url for example - https://api.radiokampus.fm/playlista/?day=20200223
    """
    r = __download_json(url)
    tracks = __prepare_list_of_tracks(r)
    return tracks


if __name__ == "__main__":
    r = __download_json("https://api.radiokampus.fm/playlista/?day=20200223")
    tracks = __prepare_list_of_tracks(r)
    print(tracks)
