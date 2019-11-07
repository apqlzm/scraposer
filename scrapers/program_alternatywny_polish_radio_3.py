"""
Extract songs from Program Alternatywny Trójki (https://www.polskieradio.pl/9/336)
Example playlist: 
https://www.polskieradio.pl/9/336/Artykul/2395504,Program-alternatywny-31-pazdziernika-godz-2007
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
    box_tracks = soup.find_all("div", "boxTrack")
    for box_track in box_tracks:
        artist = box_track.find("span", "bArtist").text.strip()
        track_name = box_track.find("span", "bTitle").text.strip()
        tracks.append(SpotifyTrack(name=track_name, artist=artist))
    return tracks


def tracks(url):
    r = __download_html(url)
    tracks = __prepare_list_of_tracks(r)
    return tracks


if __name__ == "__main__":
    r = __download_html(
        "https://www.polskieradio.pl/9/336/Artykul/2395504,Program-alternatywny-31-pazdziernika-godz-2007"
    )
    tracks = __prepare_list_of_tracks(r)
    print(tracks)
