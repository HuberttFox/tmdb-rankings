import requests
import csv
from lxml import html

import config

TMDB_BASE_URL = 'https://www.themoviedb.org'
TMDB_TOP_URL_1 = 'https://www.themoviedb.org/movie/top-rated'
TMDB_TOP_URL_2 = 'https://www.themoviedb.org/discover/movie/items'


def get_movie_info(movie_info_url):
    """获取电影详细信息"""
    print(f"  [INFO] 获取: {movie_info_url}")
    response = requests.get(movie_info_url, timeout=config.TIMEOUT)

    if response.status_code != 200:
        print(f"  [ERROR] 请求失败，状态码: {response.status_code}")
        return None

    movie_doc = html.fromstring(response.text)

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

    movie_info = {
        "name": movie_names[0].strip() if movie_names else '',
        "year": movie_years[0].strip() if movie_years else '',
        "publish_date": movie_publish_dates[0].strip() if movie_publish_dates else '',
        "score": movie_scores[0].strip() if movie_scores else '',
        "description": movie_descriptions[0].strip() if movie_descriptions else '',
        "slogan": movie_slogans[0].strip() if movie_slogans else '',
        "tags": ",".join(movie_tags) if movie_tags else '',
        "cost_time": movie_cost_times[0].strip() if movie_cost_times else '',
        "language": movie_languages[0].strip() if movie_languages else '',
        "director": ",".join(movie_directors) if movie_directors else '',
        "novel": ",".join(movie_novels) if movie_novels else ''
    }

    name = movie_info['name'][:30] + '...' if len(movie_info['name']) > 30 else movie_info['name']
    print(f"  [OK] {name} ({movie_info['year']}) - 评分: {movie_info['score']}%")
    return movie_info


def save_all_movies(all_movies):
    """保存所有电影数据到CSV文件"""
    print(f"\n{'='*60}")
    print(f"[SAVE] 保存数据到: {config.OUTPUT_FILE}")
    print(f"[SAVE] 记录数: {len(all_movies)} 条")

    with open(config.OUTPUT_FILE, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['name', 'year', 'publish_date', 'score', 'description',
                      'slogan', 'tags', 'cost_time', 'language', 'director', 'novel']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_movies)

    print(f"[SUCCESS] ✓ 已保存 {len(all_movies)} 部电影数据")
    print(f"{'='*60}\n")


def main():
    """主函数：爬取TMDB Top Rated电影并保存到CSV"""
    all_movies = []
    total_pages = config.MAX_PAGES

    print("\n" + "="*60)
    print("TMDB Top Rated 电影爬虫")
    print(f"计划爬取页数: {total_pages} 页")
    print("="*60)

    for page_num in range(1, total_pages + 1):
        print(f"\n{'─'*60}")
        print(f"[PAGE {page_num}/{total_pages}] 正在处理第 {page_num} 页...")
        print(f"{'─'*60}")

        try:
            if page_num == 1:
                print(f"[HTTP] GET {TMDB_TOP_URL_1}")
                response = requests.get(TMDB_TOP_URL_1, timeout=config.TIMEOUT)
            else:
                print(f"[HTTP] POST {TMDB_TOP_URL_2} (page={page_num})")
                response = requests.post(
                    TMDB_TOP_URL_2,
                    data=config.build_pagination_data(page_num),
                    timeout=config.TIMEOUT,
                )

            if response.status_code != 200:
                print(f"[ERROR] 页面请求失败，状态码: {response.status_code}")
                continue

            print(f"[HTTP] 响应状态: {response.status_code} OK")

        except Exception as e:
            print(f"[ERROR] 网络请求异常: {str(e)}")
            continue

        document = html.fromstring(response.text)
        xpath_expr = (
            f"//*[@id='page_{page_num}']/div/div/"
            f"div[@class='comp:poster-card w-full bg-white border "
            f"border-light-grey hover:border-gray-300 rounded-lg shadow-lg overflow-hidden']"
        )
        movie_list = document.xpath(xpath_expr)

        if not movie_list:
            print(f"[WARNING] 第 {page_num} 页未找到电影列表，可能已到达最后一页")
            break

        print(f"[FOUND] 发现 {len(movie_list)} 部电影")

        total = len(movie_list)
        success_count = 0
        for index, movie in enumerate(movie_list, 1):
            print(f"  [{index}/{total}]", end=" ")
            movie_urls = movie.xpath("./div/div/a/@href")
            if movie_urls:
                movie_info_url = TMDB_BASE_URL + movie_urls[0]
                movie_info = get_movie_info(movie_info_url)
                if movie_info:
                    all_movies.append(movie_info)
                    success_count += 1
            else:
                print("[WARN] 无法提取链接")

        print(f"\n[SUMMARY] 第 {page_num} 页完成: 成功 {success_count}/{total} 部")

    print(f"\n{'='*60}")
    print("爬取任务完成!")
    print(f"总计获取: {len(all_movies)} 部电影")
    print(f"{'='*60}")

    if all_movies:
        save_all_movies(all_movies)
    else:
        print("[WARNING] 没有获取到任何数据，跳过保存")


if __name__ == '__main__':
    main()
