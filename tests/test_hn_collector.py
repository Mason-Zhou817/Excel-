from __future__ import annotations

from typing import Any

import pytest

from freelance_starter.hn_collector import collect_keywords, fetch_keyword


class FakeResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        return self.payload


class FakeSession:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def get(self, url: str, **kwargs: Any) -> FakeResponse:
        self.calls.append({"url": url, **kwargs})
        return FakeResponse(
            {
                "hits": [
                    {
                        "title": "Python automation idea",
                        "url": "https://example.com/python",
                        "author": "alice",
                        "points": 42,
                        "num_comments": 7,
                        "created_at": "2026-01-01T00:00:00Z",
                    }
                ]
            }
        )


def test_fetch_keyword_normalizes_hacker_news_hits() -> None:
    session = FakeSession()

    rows = fetch_keyword("python", session=session, limit=1)

    assert rows == [
        {
            "keyword": "python",
            "title": "Python automation idea",
            "url": "https://example.com/python",
            "author": "alice",
            "points": 42,
            "comments": 7,
            "created_at": "2026-01-01T00:00:00Z",
        }
    ]
    assert session.calls[0]["params"]["query"] == "python"


def test_collect_keywords_requires_at_least_one_keyword() -> None:
    with pytest.raises(ValueError, match="No keywords"):
        collect_keywords(["  "], session=FakeSession())
