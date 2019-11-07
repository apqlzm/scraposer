from scrapers import kampus_radio, lp3_polish_radio_3

DOMAIN_SCAPER = {
    "radiokampus.fm": kampus_radio,
    "lp3.polskieradio.pl": lp3_polish_radio_3,
}


def get_scraper(url):
    for dc in DOMAIN_SCAPER:
        if dc in url:
            return DOMAIN_SCAPER[dc]
