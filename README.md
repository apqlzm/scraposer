# scraposer

Scrape list of tracks from a website and save it as playlist in your Spotify account.

**Required Python 3.6+**

<p align="left">
    <img src="https://apqlzm.github.io/theme/images/icons/create_playlist_lp3.svg">
</p>

Result of above command:

<p align="left">
    <img src="https://apqlzm.github.io/theme/images/icons/playlist-lp3.png">
</p>

## Supported websites

- [Radiospacja Lista Przebojów](https://radiospacja.pl/chart/)
- ~~[Lista Przebojów Trójki](http://lp3.polskieradio.pl/)~~
- [Radio Kampus playlists](https://radiokampus.fm/playlista.php)
- ~~[Program Alternatywny Trójki](https://www.polskieradio.pl/9/336)~~

## How to use it

### First time use

1. [Register new application](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app). As Redirect URL please set "https://localhost"
2. Export app's client id and client secret (replace hashes with the ones from your app):

```shell
export CLIENT_ID="e4e3ddd9f2e5cde2dad7361ca96bfa50"
export CLIENT_SECRET="78e80fed2078c427459d7053c640bdab"

```

Your are ready to go.

### Create your first playlist

To create a playlist you need a `link to a website` with list of tracks (obviously), `name` of the playlist and your Spotify `username`. Example usage:

```shell
python scraposer.py --url "https://radiospacja.pl/chart/lista-przebojow-13/" --playlist "some_name_whatever" --username "yournick"
```
