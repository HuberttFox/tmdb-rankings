import requests
import csv
from lxml import html

# Constants
TMDB_BASE_URL = 'https://www.themoviedb.org'
TMDB_TOP_URL = 'https://www.themoviedb.org/movie/top-rated'

# Main Function
def main():
    # Get the top 100 movies from IMDB
    response = requests.get(TMDB_TOP_URL, timeout=60)

    # Parse the data to retrieve the movie list
    document = html.fromstring(response.text)

    # Trverse the movie list to retrieve movie
    

    # Save the movie data to a CSV file

if __name__ == '__main__':
    main()