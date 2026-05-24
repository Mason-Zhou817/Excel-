from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
import requests

from freelance_starter.paths import ensure_parent, project_path

HACKER_NEWS_SEARCH_URL = "https://hn.algolia.com/api/v1/search"


def normalize_story(keyword: str, hit: dict[str, Any]) -> dict[str, Any]:
    return {
        "keyword": keyword,
        "title": hit.get("title") or hit.get("story_title") or "",
        "url": hit.get("url") or hit.get("story_url") or "",
        "author": hit.get("author") or "",
        "points": hit.get("points") or 0,
        "comments": hit.get("num_comments") or 0,
        "created_at": hit.get("created_at") or "",
    }


def fetch_keyword(
    keyword: str,
    *,
    limit: int = 20,
    session: Any = requests,
    timeout: int = 20,
) -> list[dict[str, Any]]:
    keyword = keyword.strip()
    if not keyword:
        raise ValueError("keyword cannot be empty")
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")

    response = session.get(
        HACKER_NEWS_SEARCH_URL,
        params={"query": keyword, "tags": "story", "hitsPerPage": limit},
        headers={"User-Agent": "python-freelance-starter/1.0"},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    hits = payload.get("hits", [])
    return [normalize_story(keyword, hit) for hit in hits[:limit]]


def collect_keywords(
    keywords: Iterable[str],
    *,
    limit: int = 20,
    session: Any = requests,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for keyword in keywords:
        if keyword.strip():
            rows.extend(fetch_keyword(keyword, limit=limit, session=session))
    if not rows:
        raise ValueError("No keywords provided.")
    return pd.DataFrame(rows)


def read_keywords(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Keyword file not found: {path}")
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def write_table(data: pd.DataFrame, output_path: Path) -> None:
    ensure_parent(output_path)
    suffix = output_path.suffix.lower()
    if suffix == ".xlsx":
        data.to_excel(output_path, index=False)
    elif suffix == ".csv":
        data.to_csv(output_path, index=False, encoding="utf-8-sig")
    else:
        raise ValueError("Output file must end with .csv or .xlsx")


def parse_args() -> argparse.Namespace:
    default_keywords = project_path("projects", "02_public_data_collector", "input", "keywords.txt")
    default_output = project_path(
        "projects", "02_public_data_collector", "output", "hn_stories.csv"
    )

    parser = argparse.ArgumentParser(
        description="Collect public Hacker News search results for keywords."
    )
    parser.add_argument("--keyword", action="append", default=[])
    parser.add_argument("--keywords-file", type=Path, default=default_keywords)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output", type=Path, default=default_output)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    keywords = args.keyword or read_keywords(args.keywords_file)
    data = collect_keywords(keywords, limit=args.limit)
    write_table(data, args.output)
    print(f"Collected {len(data)} rows for {len(keywords)} keyword(s): {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
