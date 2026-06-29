import requests
import csv
from lxml import html

# Constants
MOVIE_LIST_FILE = "csv_data/movie_list.csv"
TMDB_BASE_URL = 'https://www.themoviedb.org'
TMDB_TOP_URL_1 = 'https://www.themoviedb.org/movie/top-rated'  # Top rated movies page 1
TMDB_TOP_URL_2 = 'https://www.themoviedb.org/discover/movie/items'  # Top rated movies page 2+

# Get movie info
def get_movie_info(movie_info_url):
    """获取电影详细信息"""
    print(f"  [INFO] 获取: {movie_info_url}")
    response = requests.get(movie_info_url, timeout=60)
    
    if response.status_code != 200:
        print(f"  [ERROR] 请求失败，状态码: {response.status_code}")
        return None
    
    # Parse the HTML and extract movie information
    movie_doc = html.fromstring(response.text)
    
    # Extract movie details using XPath
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

    # Build movie info dictionary
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
    
    name = movie_info['name'][:30] + '...' if len(movie_info['name']) > 30 else movie_info['name']
    print(f"  [OK] {name} ({movie_info['year']}) - 评分: {movie_info['score']}%")
    return movie_info

# Save all movies to a CSV file
def save_all_movies(all_movies):
    """保存所有电影数据到CSV文件"""
    print(f"\n{'='*60}")
    print(f"[SAVE] 保存数据到: {MOVIE_LIST_FILE}")
    print(f"[SAVE] 记录数: {len(all_movies)} 条")
    
    with open(MOVIE_LIST_FILE, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'year', 'publish_date', 'score', 'description', 'slogan', 'tags', 'cost_time', 'language', 'director', 'novel'])
        writer.writeheader()
        writer.writerows(all_movies)
    
    print(f"[SUCCESS] ✓ 已保存 {len(all_movies)} 部电影数据")
    print(f"{'='*60}\n")

# Main Function
def main():
    """主函数：爬取TMDB Top Rated电影并保存到CSV"""
    all_movies = []     # Store all movie information
    
    total_pages = 5
    
    print("\n" + "="*60)
    print("TMDB Top Rated 电影爬虫")
    print(f"计划爬取页数: {total_pages} 页")
    print("="*60)
    
    # Crawl multiple pages (1-5)
    for page_num in range(1, total_pages + 1):
        print(f"\n{'─'*60}")
        print(f"[PAGE {page_num}/{total_pages}] 正在处理第 {page_num} 页...")
        print(f"{'─'*60}")

        # Fetch movie list page
        try:
            if page_num == 1:
                # First page uses GET request
                print(f"[HTTP] GET {TMDB_TOP_URL_1}")
                response = requests.get(TMDB_TOP_URL_1, timeout=60)
            else:
                # Subsequent pages use POST request with pagination parameters
                print(f"[HTTP] POST {TMDB_TOP_URL_2} (page={page_num})")
                response = requests.post(TMDB_TOP_URL_2,
                                         f"air_date.gte=&air_date.lte=&certification=&certification_country=KR&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2026-12-29&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=KR&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400",
                                         timeout=60)
            
            if response.status_code != 200:
                print(f"[ERROR] 页面请求失败，状态码: {response.status_code}")
                continue
                
            print(f"[HTTP] 响应状态: {response.status_code} OK")

        except Exception as e:
            print(f"[ERROR] 网络请求异常: {str(e)}")
            continue

        # Parse HTML and extract movie list
        document = html.fromstring(response.text)
        movie_list = document.xpath(
            f"//*[@id='page_{page_num}']/div/div/div[@class='comp:poster-card w-full bg-white border border-light-grey hover:border-gray-300 rounded-lg shadow-lg overflow-hidden']")
        
        if not movie_list:
            print(f"[WARNING] 第 {page_num} 页未找到电影列表，可能已到达最后一页")
            break
            
        print(f"[FOUND] 发现 {len(movie_list)} 部电影")

        # Iterate through movie list and fetch details
        total = len(movie_list)
        success_count = 0
        for index, movie in enumerate(movie_list, 1):
            print(f"  [{index}/{total}]", end=" ")
            movie_urls = movie.xpath("./div/div/a/@href")
            if movie_urls:
                # Construct the movie detail URL
                movie_info_url = TMDB_BASE_URL + movie_urls[0]
                # Fetch movie details
                movie_info = get_movie_info(movie_info_url)
                if movie_info:
                    all_movies.append(movie_info)
                    success_count += 1
            else:
                print("[WARN] 无法提取链接")

        print(f"\n[SUMMARY] 第 {page_num} 页完成: 成功 {success_count}/{total} 部")

    # Final summary
    print(f"\n{'='*60}")
    print("爬取任务完成!")
    print(f"总计获取: {len(all_movies)} 部电影")
    print(f"{'='*60}")

    # Save all movie data to CSV file
    if all_movies:
        save_all_movies(all_movies)
    else:
        print("[WARNING] 没有获取到任何数据，跳过保存")

if __name__ == '__main__':
    main()