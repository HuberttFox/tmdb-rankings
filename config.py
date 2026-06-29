import os
from datetime import date

import dotenv

dotenv.load_dotenv()

# Scraping settings
MAX_PAGES = int(os.getenv("TMDB_MAX_PAGES", "5"))
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))
OUTPUT_FILE = os.getenv("CSV_OUTPUT", "csv_data/movie_list.csv")

# TMDB API filters (for paginated discover endpoint)
WATCH_REGION = os.getenv("WATCH_REGION", "KR")
MIN_VOTE_COUNT = int(os.getenv("MIN_VOTE_COUNT", "300"))
SORT_BY = os.getenv("SORT_BY", "vote_average.desc")
ORIGINAL_LANGUAGE = os.getenv("ORIGINAL_LANGUAGE", "")
RUNTIME_MIN = int(os.getenv("RUNTIME_MIN", "0"))
RUNTIME_MAX = int(os.getenv("RUNTIME_MAX", "400"))

def build_pagination_data(page: int) -> dict:
    today = date.today().isoformat()
    return {
        "air_date.gte": "",
        "air_date.lte": "",
        "certification": "",
        "certification_country": "KR",
        "debug": "",
        "first_air_date.gte": "",
        "first_air_date.lte": "",
        "include_adult": "false",
        "include_softcore": "false",
        "latest_ceremony.gte": "",
        "latest_ceremony.lte": "",
        "page": str(page),
        "primary_release_date.gte": "",
        "primary_release_date.lte": "",
        "region": "",
        "release_date.gte": "",
        "release_date.lte": today,
        "show_me": "everything",
        "sort_by": SORT_BY,
        "vote_average.gte": "0",
        "vote_average.lte": "10",
        "vote_count.gte": str(MIN_VOTE_COUNT),
        "watch_region": WATCH_REGION,
        "with_genres": "",
        "with_keywords": "",
        "with_networks": "",
        "with_origin_country": "",
        "with_original_language": ORIGINAL_LANGUAGE,
        "with_watch_monetization_types": "",
        "with_watch_providers": "",
        "with_release_type": "",
        "with_runtime.gte": str(RUNTIME_MIN),
        "with_runtime.lte": str(RUNTIME_MAX),
    }
