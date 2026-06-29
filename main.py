import requests
import csv
from lxml import html

# Constants
MOVIE_LIST_FILE = "csv_data/movie_list.csv"
TMDB_BASE_URL = 'https://www.themoviedb.org'
TMDB_TOP_URL = 'https://www.themoviedb.org/movie/top-rated'

# Get movie info
def get_movie_info(movie_info_url):
    # Send a request to retrieve data
    print(f"[DEBUG] 正在获取电影详情: {movie_info_url}")
    response = requests.get(movie_info_url, timeout=60)
    print(f"[DEBUG] 响应状态码: {response.status_code}")

    # Parse the data to retrieve the movie info
    movie_doc = html.fromstring(response.text)
    # Retrieve the movie info
    movie_names = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/h2/a/text()")
    movie_descriptions = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/div/p/text()")
    movie_scores = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[2]/div/div/div[1]/div/div[1]/div/div/@data-percent")
    movie_years = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/h2/span/text()")
    movie_publish_dates = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[2]/text()")
    movie_tags = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[3]/a/text()")
    movie_cost_times = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[4]/text()")
    movie_languages = movie_doc.xpath("/html/body/div[1]/main/section/div[3]/div/div/div[2]/div/section/div[1]/div/section[1]/p[2]/text()")
    movie_directors = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")
    movie_novels = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")
    movie_slogans = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/h3[1]/text()")

    # Return the movie info
    movie_info = {
        "name": movie_names[0].strip() if movie_names else '',
        "year": movie_years[0].strip() if movie_years else '',
        "publish_date": movie_publish_dates[0].strip() if movie_publish_dates else '',
        "score": movie_scores[0].strip() if movie_scores else '',
        "description": movie_descriptions[0].strip() if movie_descriptions else '',
        "slogan": movie_slogans[0].strip() if movie_slogans else '',
        "tags": ",".join(movie_tags) if movie_tags else '',
        "cost_time": movie_cost_times[0].strip() if movie_cost_times else '',
        "language": movie_languages[0].strip() if movie_languages else '',        "director": ",".join(movie_directors) if movie_directors else '',
        "novel": ",".join(movie_novels) if movie_novels else ''
    }
    
    print(f"[DEBUG] 解析结果 - 名称: {movie_info['name']}, 年份: {movie_info['year']}, 评分: {movie_info['score']}")
    return movie_info

# Save all movies to a CSV file
def save_all_movies(all_movies):
    print(f"\n[DEBUG] 准备保存 {len(all_movies)} 部电影到 CSV 文件: {MOVIE_LIST_FILE}")
    with open(MOVIE_LIST_FILE, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'year', 'publish_date', 'score', 'description', 'slogan', 'tags', 'cost_time', 'language', 'director', 'novel'])
        writer.writeheader()
        writer.writerows(all_movies)
    print(f"[DEBUG] ✓ 成功保存 {len(all_movies)} 部电影数据\n")

# Main Function
def main():
    print("="*60)
    print("[DEBUG] 开始爬取 TMDB Top Rated 电影")
    print(f"[DEBUG] 目标URL: {TMDB_TOP_URL}")
    print("="*60)
    
    # Get the top 100 movies from IMDB
    print("\n[DEBUG] 步骤1: 获取电影列表页面...")
    response = requests.get(TMDB_TOP_URL, timeout=60)
    print(f"[DEBUG] 列表页面响应状态码: {response.status_code}")

    # Parse the data to retrieve the movie list
    document = html.fromstring(response.text)
    movie_list = document.xpath("//*[@class='comp:poster-card w-full bg-white border border-light-grey hover:border-gray-300 rounded-lg shadow-lg overflow-hidden']")
    print(f"[DEBUG] 找到 {len(movie_list)} 部电影")

    # Trverse the movie list to retrieve movie
    all_movies = []
    total = len(movie_list)
    for index, movie in enumerate(movie_list, 1):
        print(f"\n[DEBUG] 进度: [{index}/{total}]")
        movie_urls = movie.xpath("./div/div/a/@href")
        if movie_urls:
            # Construct the movie info URL
            movie_info_url = TMDB_BASE_URL + movie_urls[0]
            # Get the movie info
            movie_info = get_movie_info(movie_info_url)
            all_movies.append(movie_info)
        else:
            print(f"[WARNING] 无法提取第 {index} 部电影的链接")

    print("\n" + "="*60)
    print(f"[DEBUG] 爬取完成! 共获取 {len(all_movies)} 部电影信息")
    print("="*60)

    # Save the movie data to a CSV file
    save_all_movies(all_movies)

if __name__ == '__main__':
    main()