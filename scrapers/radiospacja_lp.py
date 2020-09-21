"""
Extract songs from https://radiospacja.pl/chart/lista-przebojow-xxx
"""

import requests
from bs4 import BeautifulSoup

from scrapers.models import SpotifyTrack


def __download_html(url):
    result = requests.get(url)
    return result.content


def __prepare_list_of_tracks(html):
    tracks = []
    soup = BeautifulSoup(html, "lxml")
    tracks_divs = soup.find_all("div", "qt-titles")
    for track_div in tracks_divs:
        track_name = track_div.find_all("h4")[0].text
        artist = track_div.find_all("p")[0].text
        tracks.append(SpotifyTrack(name=track_name, artist=artist))
    return tracks


def tracks(url):
    r = __download_html(url)
    tracks = __prepare_list_of_tracks(r)
    return tracks


if __name__ == "__main__":
    r = __download_html("https://radiospacja.pl/chart/lista-przebojow-13/")
    tracks = __prepare_list_of_tracks(r)
    print(tracks)
