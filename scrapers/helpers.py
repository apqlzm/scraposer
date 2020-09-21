from scrapers import (
    kampus_radio,
    load_json,
    radiospacja_lp,
)

DOMAIN_SCAPER = {
    "radiokampus.fm": kampus_radio,
    "radiospacja.pl": radiospacja_lp,
    ".json": load_json,  # load data from file
}


def get_scraper(url):
    for dc in DOMAIN_SCAPER:
        if dc in url:
            return DOMAIN_SCAPER[dc]
