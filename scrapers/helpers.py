from scrapers import (
    kampus_radio,
    load_json,
    lp3_polish_radio_3,
    program_alternatywny_polish_radio_3,
    radiospacja_lp,
)

DOMAIN_SCAPER = {
    "radiokampus.fm": kampus_radio,
    "lp3.polskieradio.pl": lp3_polish_radio_3,
    "polskieradio.pl/9/336": program_alternatywny_polish_radio_3,
    "radiospacja.pl": radiospacja_lp,
    ".json": load_json,  # load data from file
}


def get_scraper(url):
    for dc in DOMAIN_SCAPER:
        if dc in url:
            return DOMAIN_SCAPER[dc]
