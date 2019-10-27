from script import SpotifyConnector


def test_extract_authorization_code_from_url():
    connector = SpotifyConnector()
    code = connector._extract_authorization_code_from_url(
        (
            "https://localhost/?code=AQB5geYwjc0NP9SuDD8WdDzLV1sZGLNB8UvTg1ppg4"
            "VJ7hRlGJEwvtkS5ffD5ykCV1uWqsCN_Mys6D4mJDXDqPbFC866ELtDYudd7KKYAE9T"
            "-l2a2FLnatWrNqU4WfC6EKTk5IPyfO0bD-KKoW0F0kepdERLTuSw5zg30hcHtUDXjL"
            "BUUaDH6jsaUxmSXvUylLx-NVDvGR7tcf6PoyQ6taU_bewd7PmRmH1jWxxmLSkX90g&"
            "state=kmlads23r2k13lm90dask"
        )
    )
    assert code == (
        "AQB5geYwjc0NP9SuDD8WdDzLV1sZGLNB8UvTg1ppg4VJ7hRlGJEwvtkS5f"
        "fD5ykCV1uWqsCN_Mys6D4mJDXDqPbFC866ELtDYudd7KKYAE9T-l2a2FLn"
        "atWrNqU4WfC6EKTk5IPyfO0bD-KKoW0F0kepdERLTuSw5zg30hcHtUDXjL"
        "BUUaDH6jsaUxmSXvUylLx-NVDvGR7tcf6PoyQ6taU_bewd7PmRmH1jWxxm"
        "LSkX90g"
    )
