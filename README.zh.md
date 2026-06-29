> [English Version](README.md)

# TMDB Rankings

爬取 [TMDB](https://www.themoviedb.org) 最高评分电影排行榜，输出结构化 CSV 数据。

## 功能

- 爬取 TMDB 最高评分电影列表页面
- 提取每部电影的详细信息：
  - 名称、年份、上映日期
  - 评分（观众评分百分比）
  - 简介、标语
  - 标签/分类、时长
  - 语言、导演、编剧
- 输出整洁的 CSV 文件

## 环境要求

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/)（包管理器）

## 安装

```bash
git clone <repo-url>
cd tmdb-rankings
uv sync
```

## 使用

```bash
uv run main.py
```

结果将保存到 `csv_data/movie_list.csv`。

### CSV 字段说明

| 字段 | 说明 |
|---|---|
| name | 电影名称 |
| year | 上映年份 |
| publish_date | 完整上映日期 |
| score | 观众评分 (0-100) |
| description | 剧情简介 |
| slogan | 宣传标语 |
| tags | 分类标签（逗号分隔） |
| cost_time | 片长 |
| language | 语言 |
| director | 导演 |
| novel | 编剧/原著作者 |

## 项目结构

```
tmdb-rankings/
├── main.py          # 入口文件
├── pyproject.toml   # 项目配置与依赖
├── csv_data/        # 输出目录（已忽略）
└── .gitignore
```

## 许可

MIT
