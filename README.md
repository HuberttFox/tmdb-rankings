> [中文版](README.zh.md)

# TMDB Rankings

Scrape [TMDB](https://www.themoviedb.org) top-rated movie rankings and export structured data to CSV.

## Features

- Scrapes TMDB's top-rated movie list page
- Extracts detailed metadata for each movie:
  - Name, year, publish date
  - Score (audience rating percentage)
  - Description, tagline/slogan
  - Tags/categories, runtime
  - Language, director, novelist
- Outputs clean CSV with all fields

## Requirements

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) (package manager)

## Setup

```bash
git clone <repo-url>
cd tmdb-rankings
uv sync
```

## Usage

```bash
uv run main.py
```

Output will be saved to `csv_data/movie_list.csv`.

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
├── pyproject.toml   # Project config & dependencies
├── csv_data/        # Output directory (gitignored)
└── .gitignore
```

## License

MIT
