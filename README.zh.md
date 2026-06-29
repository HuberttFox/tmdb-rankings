> [English Version](README.md)

# TMDB Rankings

爬取 [TMDB](https://www.themoviedb.org) 最高评分电影排行榜，输出结构化 CSV 数据。

## 功能

- 多页爬取 TMDB 最高评分电影列表
- 提取每部电影的详细信息：
  - 名称、年份、上映日期
  - 评分（观众评分百分比）
  - 简介、标语
  - 标签/分类、时长
  - 语言、导演、编剧
- 分页支持（可配置页数）
- 错误处理与逐页进度追踪
- 输出整洁的 CSV 文件

## 环境要求

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/)（包管理器）

## 安装

```bash
git clone <repo-url>
cd tmdb-rankings
uv sync
cp .env.example .env   # 可选：自定义配置
```

## 配置

所有可配置项位于 `.env`（从 `.env.example` 复制）：

| 变量 | 默认值 | 说明 |
|---|---|---|
| `TMDB_MAX_PAGES` | `5` | 爬取页数 |
| `REQUEST_TIMEOUT` | `60` | HTTP 请求超时（秒） |
| `CSV_OUTPUT` | `csv_data/movie_list.csv` | 输出文件路径 |
| `WATCH_REGION` | `KR` | ISO-3166 地区代码 |
| `MIN_VOTE_COUNT` | `300` | 最低投票数阈值 |
| `SORT_BY` | `vote_average.desc` | 排序方式 |
| `ORIGINAL_LANGUAGE` | *(空)* | 按原始语言过滤 |
| `RUNTIME_MIN` / `RUNTIME_MAX` | `0` / `400` | 片长范围（分钟） |

## 使用

```bash
uv run main.py
```

结果将保存到 `csv_data/movie_list.csv`（或你配置的路径）。

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
├── config.py        # 配置加载
├── pyproject.toml   # 项目配置与依赖
├── .env.example     # 示例环境配置
├── csv_data/        # 输出目录（已忽略）
└── .gitignore
```

## 注意事项

- XPath 选择器依赖 TMDB 当前 DOM 结构，网站改版后可能失效
- 第 1 页使用 `/movie/top-rated` 端点，后续页使用 `/discover/movie/items` API
- `release_date.lte` 过滤条件自动设为当天日期

## 许可

MIT
