"""
Extract songs from https://radiokampus.fm/playlista.php
"""

import re

import requests
from bs4 import BeautifulSoup

from scrapers.models import SpotifyTrack


def __download_html(url):
    result = requests.get(url)
    return result.content


def __prepare_list_of_tracks(html):
    tracks = []
    soup = BeautifulSoup(html, "lxml")
    div_with_table = soup.find("div", "art_view_full view_full")
    rows = div_with_table.find_all("tr")
    for row in rows:
        tds = row.find_all("td")
        if tds[1].b:
            artist = tds[1].b.text
            artist_track = tds[1].text
            track_name = artist_track.replace(artist, "")
            track_name = track_name.strip()[1:]
            # sometimes there is a text in braces with feat. artists
            # finding such tracks is impossible
            track_name = re.sub(r"\(.*?\)", "", track_name).strip()
            tracks.append(SpotifyTrack(name=track_name, artist=artist))
    return tracks


def tracks(url):
    r = __download_html(url)
    tracks = __prepare_list_of_tracks(r)
    return tracks


if __name__ == "__main__":
    r = __download_html("https://radiokampus.fm/playlista.php")
    tracks = __prepare_list_of_tracks(r)
    print(tracks)
