from __future__ import annotations

import pandas as pd

from freelance_starter.excel_report import (
    clean_orders,
    summarize_by_category,
    summarize_by_month,
)


def test_clean_orders_drops_bad_rows_and_deduplicates_order_ids() -> None:
    raw_orders = pd.DataFrame(
        [
            {
                "order_id": " A-1 ",
                "date": "2026-01-01",
                "customer": "Acme ",
                "product": "Keyboard",
                "category": "Electronics",
                "region": "East",
                "salesperson": "Alice",
                "quantity": "2",
                "unit_price": "10",
                "source_file": "a.csv",
            },
            {
                "order_id": "A-1",
                "date": "2026-01-02",
                "customer": "Acme",
                "product": "Keyboard",
                "category": "Electronics",
                "region": "East",
                "salesperson": "Alice",
                "quantity": "3",
                "unit_price": "10",
                "source_file": "b.csv",
            },
            {
                "order_id": "A-2",
                "date": "not-a-date",
                "customer": "Acme",
                "product": "Mouse",
                "category": "Electronics",
                "region": "East",
                "salesperson": "Alice",
                "quantity": "1",
                "unit_price": "5",
                "source_file": "b.csv",
            },
        ]
    )

    cleaned = clean_orders(raw_orders)

    assert len(cleaned) == 1
    assert cleaned.loc[0, "order_id"] == "A-1"
    assert cleaned.loc[0, "quantity"] == 3
    assert cleaned.loc[0, "revenue"] == 30


def test_summaries_group_by_category_and_month() -> None:
    cleaned = pd.DataFrame(
        [
            {
                "order_id": "A-1",
                "date": pd.Timestamp("2026-01-01"),
                "month": "2026-01",
                "category": "Office",
                "quantity": 2,
                "revenue": 20.0,
            },
            {
                "order_id": "A-2",
                "date": pd.Timestamp("2026-01-02"),
                "month": "2026-01",
                "category": "Office",
                "quantity": 3,
                "revenue": 30.0,
            },
        ]
    )

    category_summary = summarize_by_category(cleaned)
    monthly_summary = summarize_by_month(cleaned)

    assert category_summary.loc[0, "category"] == "Office"
    assert category_summary.loc[0, "revenue"] == 50.0
    assert monthly_summary.loc[0, "orders"] == 2
    assert monthly_summary.loc[0, "quantity"] == 5
