"""
Compose Spotify playlist by scraping websites
"""

import datetime
import os
import pickle
import re
from dataclasses import dataclass
from typing import Optional

import requests



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
    def authorise_url(self):
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
    def _extract_authorization_code_from_url(url_with_code):
        match = re.search(r"code=(.*?)(&|$)", url_with_code)
        authorization_code = match.group(1)
        return authorization_code

    def generate_authorization_code(self):
        """ Generate authorization code and grand permissions to application. 

        1st step of authorization process.
        """
        redirect_url = input(
            (
                "Log in and accept permissions then you'll be redirected "
                "to localhost url. Copy the address and pasted it here: "
                "Follow authorisation url:\n {authorise_url} "
            ).format(authorise_url=self.authorise_url)
        )
        self.authorization_code = self._extract_authorization_code_from_url(
            redirect_url
        )

    def generate_access_and_refresh_tokens(self):
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

    def refresh_access_token(self):
        """ Refresh access token when expired.

        3rd step and repeated every hour. Interval between every refresh is done
        every `access_token_expires_in` seconds.
        """
        response = self.session.post(
            self.API_TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": "",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )


if __name__ == "__main__":
    # TODO: work in progress
    # 1. Does file with serialized connector exist
    #   YES -> load file and check if token expired. Refresh token if needed.
    #   NO -> Do whole authentication from begin.
    connector = SpotifyConnector()
    connector.generate_authorization_code()
    connector.generate_access_and_refresh_tokens()
    print(connector)
