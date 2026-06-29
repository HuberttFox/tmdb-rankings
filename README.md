> [中文版](README.zh.md)

# TMDB Rankings

Scrape [TMDB](https://www.themoviedb.org) top-rated movie rankings and export structured data to CSV.

## Features

- Scrapes TMDB's top-rated movie list across multiple pages
- Extracts detailed metadata for each movie:
  - Name, year, publish date
  - Score (audience rating percentage)
  - Description, tagline/slogan
  - Tags/categories, runtime
  - Language, director, novelist
- Pagination support (configurable page count)
- Error handling with per-page progress tracking
- Outputs clean CSV with all fields

## Requirements

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) (package manager)

## Setup

```bash
git clone <repo-url>
cd tmdb-rankings
uv sync
cp .env.example .env   # Optional: customize configuration
```

## Configuration

All configurable options are in `.env` (copy from `.env.example`):

| Variable | Default | Description |
|---|---|---|
| `TMDB_MAX_PAGES` | `5` | Number of pages to crawl |
| `REQUEST_TIMEOUT` | `60` | HTTP request timeout (seconds) |
| `CSV_OUTPUT` | `csv_data/movie_list.csv` | Output file path |
| `WATCH_REGION` | `KR` | ISO-3166 region code for filtering |
| `MIN_VOTE_COUNT` | `300` | Minimum vote count threshold |
| `SORT_BY` | `vote_average.desc` | Sort order |
| `ORIGINAL_LANGUAGE` | *(empty)* | Filter by original language |
| `RUNTIME_MIN` / `RUNTIME_MAX` | `0` / `400` | Runtime range (minutes) |

## Usage

```bash
uv run main.py
```

Output will be saved to `csv_data/movie_list.csv` (or your configured path).

### CSV Fields

| Field | Description |
|---|---|
| name | Movie title |
| year | Release year |
| publish_date | Full release date |
| score | Audience score (0-100) |
| description | Plot summary |
| slogan | Tagline |
| tags | Comma-separated genre tags |
| cost_time | Runtime |
| language | Language |
| director | Director(s) |
| novel | Novelist(s) / screenplay |

## Project Structure

```
tmdb-rankings/
├── main.py          # Entry point
├── config.py        # Configuration loader
├── pyproject.toml   # Project config & dependencies
├── .env.example     # Example environment config
├── csv_data/        # Output directory (gitignored)
└── .gitignore
```

## Notes

- XPath selectors depend on TMDB's current DOM structure and may break after site updates.
- Page 1 uses the `/movie/top-rated` endpoint; subsequent pages use the `/discover/movie/items` API.
- The `release_date.lte` filter is automatically set to today's date.

## License

MIT
