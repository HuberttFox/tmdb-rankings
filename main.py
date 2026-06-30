import requests
import csv
from lxml import html
import re
import config

TMDB_BASE_URL = 'https://www.themoviedb.org'
TMDB_TOP_URL_1 = 'https://www.themoviedb.org/movie/top-rated'
TMDB_TOP_URL_2 = 'https://www.themoviedb.org/discover/movie/items'


def get_movie_year(movie_years):
    raw = movie_years[0].strip() if movie_years else ''
    return raw.strip("()")


def get_movie_publish_data(movie_publish_dates):
    raw = movie_publish_dates[0].strip() if movie_publish_dates else ''
    match = re.search(r"\d{4}-\d{2}-\d{2}", raw)
    return match.group() if match else ''


def get_movie_cost_time(movie_cost_times):
    raw = movie_cost_times[0].strip() if movie_cost_times else ''
    h = int(m) if (m := re.search(r"(\d+)h", raw)) else 0
    m = int(m) if (m := re.search(r"(\d+)m", raw)) else 0
    return h * 60 + m


def get_movie_info(movie_info_url):
    print(f"  [DL] {movie_info_url}")
    response = requests.get(movie_info_url, timeout=config.TIMEOUT)

    if response.status_code != 200:
        print(f"  [ERR] HTTP {response.status_code}")
        return None

    movie_doc = html.fromstring(response.text)
    movie_names = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/h2/a/text()")
    movie_descriptions = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/div/p/text()")
    movie_scores = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[2]/div/div/div[1]/div/div[1]/div/div/@data-percent")
    movie_years = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/h2/span/text()")
    movie_publish_dates = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[@class='release']/text()")
    movie_tags = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[@class='genres']/a/text()")
    movie_cost_times = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[@class='runtime']/text()")
    movie_languages = movie_doc.xpath("/html/body/div[1]/main/section/div[3]/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")
    movie_directors = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")
    movie_novels = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")
    movie_slogans = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/h3[1]/text()")

    info = {
        "name": movie_names[0].strip() if movie_names else '',
        "year": get_movie_year(movie_years),
        "publish_date": get_movie_publish_data(movie_publish_dates),
        "score": movie_scores[0].strip() if movie_scores else '',
        "description": movie_descriptions[0].strip() if movie_descriptions else '',
        "slogan": movie_slogans[0].strip() if movie_slogans else '',
        "tags": ",".join(movie_tags) if movie_tags else '',
        "cost_time": get_movie_cost_time(movie_cost_times),
        "language": movie_languages[0].strip() if movie_languages else '',
        "director": ",".join(movie_directors) if movie_directors else '',
        "novel": ",".join(movie_novels) if movie_novels else ''
    }

    name = info['name'][:30] + '...' if len(info['name']) > 30 else info['name']
    print(f"  [OK] {name} ({info['year']}) {info['score']}%")
    return info


def save_all_movies(all_movies):
    print(f"\n{'='*60}")
    print(f"[SAVE] {config.OUTPUT_FILE} ({len(all_movies)} 条)")

    with open(config.OUTPUT_FILE, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['name', 'year', 'publish_date', 'score', 'description',
                      'slogan', 'tags', 'cost_time', 'language', 'director', 'novel']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_movies)

    print(f"[DONE] ✓ 已保存 {len(all_movies)} 部电影数据")
    print(f"{'='*60}\n")


def main():
    all_movies = []
    total_pages = config.MAX_PAGES

    print(f"\n{'='*60}")
    print(f"TMDB Top Rated  页数: {total_pages}")
    print(f"{'='*60}")

    for page_num in range(1, total_pages + 1):
        print(f"\n{'─'*60}")
        print(f"第 {page_num}/{total_pages} 页")
        print(f"{'─'*60}")

        try:
            if page_num == 1:
                response = requests.get(TMDB_TOP_URL_1, timeout=config.TIMEOUT)
            else:
                response = requests.post(
                    TMDB_TOP_URL_2,
                    data=config.build_pagination_data(page_num),
                    timeout=config.TIMEOUT,
                )

            if response.status_code != 200:
                print(f"[ERR] HTTP {response.status_code}")
                continue

        except Exception as e:
            print(f"[ERR] {e}")
            continue

        document = html.fromstring(response.text)
        xpath_expr = (
            f"//*[@id='page_{page_num}']/div/div/"
            f"div[@class='comp:poster-card w-full bg-white border "
            f"border-light-grey hover:border-gray-300 rounded-lg shadow-lg overflow-hidden']"
        )
        movie_list = document.xpath(xpath_expr)

        if not movie_list:
            print(f"[WARN] 第 {page_num} 页无数据，已结束")
            break

        print(f"[PAGE] {len(movie_list)} 部")

        success_count = 0
        for index, movie in enumerate(movie_list, 1):
            print(f"  [{index}/{len(movie_list)}]", end=" ")
            movie_urls = movie.xpath("./div/div/a/@href")
            if movie_urls:
                info = get_movie_info(TMDB_BASE_URL + movie_urls[0])
                if info:
                    all_movies.append(info)
                    success_count += 1
            else:
                print("[WARN] 无链接")

        print(f"\n[PG-OK] 第 {page_num} 页: {success_count}/{len(movie_list)}")

    print(f"\n{'='*60}")
    print(f"总计: {len(all_movies)} 部")
    print(f"{'='*60}")

    if all_movies:
        save_all_movies(all_movies)
    else:
        print("[WARN] 无数据")


if __name__ == '__main__':
    main()
