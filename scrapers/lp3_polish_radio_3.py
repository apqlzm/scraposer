"""
Extract songs from http://lp3.polskieradio.pl/
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
    div_center = soup.find("div", id="divCenter")
    div_chart = div_center.find("div", "boxNotowanie")
    box_tracks = div_chart.find_all("div", "BoxTrack")
    for box_track in box_tracks:
        box_track_links = box_track.find_all("a")
        artist = box_track_links[0].text
        track_name = box_track_links[1].text
        tracks.append(SpotifyTrack(name=track_name, artist=artist))
    return tracks


def tracks(url):
    r = __download_html(url)
    tracks = __prepare_list_of_tracks(r)
    return tracks


if __name__ == "__main__":
    r = __download_html("http://lp3.polskieradio.pl/")
    tracks = __prepare_list_of_tracks(r)
    print(tracks)
