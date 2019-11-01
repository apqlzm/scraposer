# scraposer

Scrape list of tracks from a website and save it as playlist in your Spotify account.

At the moment only [Lista Przebojów Trójki](http://lp3.polskieradio.pl/) is supported.
Other websites may be added in future.

**Required Python 3.6+**

<p align="left">
    <img src="https://apqlzm.github.io/theme/images/icons/create_playlist_lp3.svg">
</p>

## How to use it

### First time use

It's simple command line tool so there is no hosted website which would allow users to authorize to my Spotify application. So you need to use your own Spotify app.

1. Register new application - [link to instruction](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app). As Redirect URL please set "https://localhost"
2. Export app's client id and client secret (replace hashes with the ones from your app):

```shell
export CLIENT_ID="e4e3ddd9f2e5cde2dad7361ca96bfa50"
export CLIENT_SECRET="78e80fed2078c427459d7053c640bdab"

```

Your are ready to go.

### Create your first playlist

To create a playlist you need a lint to the website with list of tracks, you'll be also asked for name of the playlist and your Spotify username. Example usage:

```python
python scraposer.py --url "http://lp3.polskieradio.pl/notowania/?rok=2014&numer=1681" --playlist "some_name_whatever" --username "yournick"
```