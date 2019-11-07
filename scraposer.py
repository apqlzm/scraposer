"""
Compose Spotify playlist by scraping websites
"""

import datetime
import os
import pickle
import re
from dataclasses import dataclass
from typing import List, Optional

import click
import requests

from scrapers.helpers import get_scraper
from scrapers.models import SpotifyTrack

SERIALIZED_OBJ = "serialized_obj"


class AuthorisationException(Exception):
    """ All kind of problems related to authorisation or token generation """


@dataclass
class SpotifyConnector:
    """ Create connection to Spotify API 

    Implementation of authorisation code flow based on:
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow
    Authorisation steps:
    1. Initialize application by sending request to 
    `GET https://accounts.spotify.com/authorize`

    Example request:
    https://accounts.spotify.com/authorize?client_id=c48f8c867a844d5da98c2a50f3c67b31&response_type=code&redirect_uri=https%3A%2F%2Flocalhost&scope=playlist-modify-private%20user-read-email&state=kmlads23r2k13lm90dask

    2. Exchange authorisation code for access and refresh tokens
    3. Refresh authorisation code when expired
    """

    access_token: str = ""
    refresh_token: str = ""
    access_token_generated_time: Optional[datetime.datetime] = None
    access_token_expires_in: int = 0
    session: requests.Session = requests.Session()
    client_id: Optional[str] = os.environ.get("CLIENT_ID")
    client_secret: Optional[str] = os.environ.get("CLIENT_SECRET")

    _instance = None
    REDIRECT_URI = "https://localhost"
    API_TOKEN_URL = "https://accounts.spotify.com/api/token"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpotifyConnector, cls).__new__(cls)
        return cls._instance

    @property
    def __authorise_url(self):
        return (
            "https://accounts.spotify.com/authorize?client_id={client_id}"
            "&response_type={response_type}"
            "&redirect_uri={redirect_uri}"
            "&scope={scope}"
            "&state={state}"
        ).format(
            client_id=self.client_id,
            response_type="code",
            redirect_uri=self.REDIRECT_URI,
            scope="playlist-modify-private",
            state="kmlads23r2k13lm90dask",  # FIXME make it random
        )

    @staticmethod
    def _extract_authorization_code_from_url(url_with_code: str):
        match = re.search(r"code=(.*?)(&|$)", url_with_code)
        if match:
            authorization_code = match.group(1)
            return authorization_code
        raise AuthorisationException("Authorization code not found in url")

    def __generate_authorization_code(self):
        """ Generate authorization code and grand permissions to application. 

        1st step of authorization process.
        """
        if not self.client_id or not self.client_secret:
            raise AuthorisationException(
                "CLIENT_ID or CLIENT_SECRET were not in environment variable list. "
                "Use `export` command to fix it"
            )
        redirect_url = input(
            (
                "Log in and accept permissions then you'll be redirected "
                "to localhost url. Copy the address and pasted it here: "
                "Follow authorisation url:\n {authorise_url} "
            ).format(authorise_url=self.__authorise_url)
        )
        self.authorization_code = self._extract_authorization_code_from_url(
            redirect_url
        )

    def __generate_access_and_refresh_tokens(self):
        """ Obtain access and refresh tokens.

        2nd step of authorisation process.
        At this moment we have code (authorisation code from step one), 
        client_id and client_secret (both copied from application dashboard).
        Now we need to obtain authorisation_token and refresh_token and that is
        the purpose of the method.
        """
        response = self.session.post(
            self.API_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": self.authorization_code,
                "redirect_uri": self.REDIRECT_URI,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        if response.status_code == 200:
            data_dict = response.json()
            self.access_token = data_dict.get("access_token")
            self.refresh_token = data_dict.get("refresh_token")
            self.access_token_expires_in = data_dict.get("expires_in")
            self.access_token_generated_time = datetime.datetime.now()
        else:
            raise AuthorisationException("Generate access token failed")

    def __refresh_access_token(self):
        """ Refresh access token when expired.

        3rd step and repeated every hour. Interval between every refresh is done
        every `access_token_expires_in` seconds.
        """
        response = self.session.post(
            self.API_TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        if response.status_code == 200:
            data_dict = response.json()
            self.access_token = data_dict.get("access_token")
            self.access_token_expires_in = data_dict.get("expires_in")
            self.access_token_generated_time = datetime.datetime.now()
        else:
            raise AuthorisationException("Refreshing access token failed")

    def initialize(self):
        try:
            self.__generate_authorization_code()
        except AttributeError:
            raise AuthorisationException(
                "Could not generate authorization code. Did you paste link?"
            )
        self.__generate_access_and_refresh_tokens()

    def get_access_token(self):
        diff = datetime.datetime.now() - self.access_token_generated_time
        if diff >= datetime.timedelta(seconds=self.access_token_expires_in - 1):
            self.__refresh_access_token()
        return self.access_token


def find_track(
    artist: str, track: str, connector: SpotifyConnector
) -> requests.Response:
    url = "https://api.spotify.com/v1/search"
    session = connector.session
    response = session.get(
        url,
        params={"q": f"artist:{artist} track:{track}", "type": "track"},
        headers={
            "Authorization": "Bearer {access_token}".format(
                access_token=connector.get_access_token()
            )
        },
    )
    return response


def create_playlist(
    name: str, username: str, connector: SpotifyConnector
) -> Optional[str]:
    url = "https://api.spotify.com/v1/users/{user_id}/playlists".format(
        user_id=f"{username}"
    )
    result = connector.session.post(
        url,
        headers={
            "Authorization": "Bearer {access_token}".format(
                access_token=connector.get_access_token()
            )
        },
        json={"name": name, "public": False},
    )
    if result.status_code in (200, 201):
        data_dict = result.json()
        return data_dict["id"]
    return None


def add_tracks_to_playlist(
    playlist_id: str, tracks: List[SpotifyTrack], connector: SpotifyConnector
) -> Optional[str]:
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    result = connector.session.post(
        url,
        headers={
            "Authorization": "Bearer {access_token}".format(
                access_token=connector.get_access_token()
            )
        },
        json={"uris": [track.uri for track in tracks if track.uri]},
    )

    if result.status_code in (200, 201):
        data_dict = result.json()
        return data_dict["snapshot_id"]
    return None


def initialize_connector() -> SpotifyConnector:
    try:
        connector = deserialize_obj()
    except FileNotFoundError:
        connector = SpotifyConnector()
        connector.initialize()
        serialize_obj(connector)
    return connector


def split_up_list(the_list: list, group_len: int) -> List[list]:
    output = []
    left_idx = 0
    right_idx = group_len
    while True:
        group = the_list[left_idx:right_idx]
        if group:
            output.append(group)
        else:
            return output
        left_idx += group_len
        right_idx += group_len


def process_track(track: SpotifyTrack, connector: SpotifyConnector) -> None:
    res = find_track(track.artist, track.name, connector)
    if res.status_code != 200:
        click.echo(
            click.style(f"Failed searching: {track.artist}, {track.name}", fg="red")
        )
        return None
    data_dict = res.json()
    total_found = data_dict["tracks"]["total"]
    if total_found == 1:
        uri = data_dict["tracks"]["items"][0]["uri"]
        track.uri = uri
        click.echo(click.style(f"{track.artist}, {track.name}: {uri}", fg="green"))
    elif total_found > 1:
        # TODO: is first item the best match?
        uri = data_dict["tracks"]["items"][0]["uri"]
        track.uri = uri
        click.echo(
            click.style(
                f"{track.artist}, {track.name} [{total_found}]: {uri}", fg="green"
            )
        )
    else:
        # TODO: ask user to modify artist or track name and search again?
        click.echo(click.style(f"Not found: {track.artist}, {track.name}", fg="red"))


def serialize_obj(obj):
    with open(SERIALIZED_OBJ, mode="wb") as f:
        pickle.dump(obj, f)


def deserialize_obj():
    with open(SERIALIZED_OBJ, mode="rb") as f:
        obj = pickle.load(f)
    return obj


@click.command()
@click.option("--url", required=True, help="Url to website with list of songs")
@click.option("--playlist", required=True, help="Name of playlist to be created")
@click.option(
    "--username",
    required=True,
    help="Username to Spotify account where the playlist will be created",
)
def main(url, playlist, username):
    connector = initialize_connector()
    scraper = get_scraper(url)
    tracks = scraper.tracks(url)

    for track in tracks:
        process_track(track, connector)

    click.echo("-----------")
    playlist_id = create_playlist(playlist, username, connector)

    # It is allowed to add maximum 100 tracks to playlist per request
    if len(tracks) <= 100:
        snapshot_id = add_tracks_to_playlist(playlist_id, tracks, connector)
    else:
        for group in split_up_list(tracks, 100):
            snapshot_id = add_tracks_to_playlist(playlist_id, group, connector)

    if snapshot_id:
        click.echo(f"Success! playlist's snapshot id: {snapshot_id}")
    else:
        click.echo(f"Failed to create playlist")
    serialize_obj(connector)


if __name__ == "__main__":
    main()
