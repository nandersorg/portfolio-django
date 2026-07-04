"""Helpers for reading and aggregating stored news sentiment data."""

from __future__ import annotations

from collections import defaultdict
from datetime import timedelta
from typing import Any

from django.db import connections
from django.utils import timezone

SENTIMENT_SCORES = {
    "POSITIVE": 1.0,
    "NEUTRAL": 0.0,
    "NEGATIVE": -1.0,
}


def _label_for_average(average_score: float | None) -> str:
    if average_score is None:
        return "NO DATA"
    if average_score > 0.25:
        return "POSITIVE"
    if average_score < -0.25:
        return "NEGATIVE"
    return "NEUTRAL"


def _summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "overall": {
                "label": "NO DATA",
                "average_score": None,
                "article_count": 0,
            },
            "categories": [],
        }

    total_score = 0.0
    per_category: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        score = SENTIMENT_SCORES.get(row["sentiment"], 0.0)
        total_score += score
        per_category[row["category"]].append(score)

    overall_average = total_score / len(rows)
    categories = []
    for category, scores in sorted(per_category.items()):
        average_score = round(sum(scores) / len(scores), 1)
        categories.append(
            {
                "category": category,
                "label": _label_for_average(average_score),
                "average_score": average_score,
                "article_count": len(scores),
            }
        )

    return {
        "overall": {
            "label": _label_for_average(overall_average),
            "average_score": round(overall_average, 1),
            "article_count": len(rows),
        },
        "categories": categories,
    }


def get_sentiment_dashboard_data() -> dict[str, Any]:
    if "analytics" not in connections.databases:
        return {
            "available": False,
            "message": "analytics database is not configured",
            "today": _summarize_rows([]),
            "windows": {
                "week": _summarize_rows([]),
                "month": _summarize_rows([]),
            },
        }

    now = timezone.now()
    today = timezone.localdate()
    week_cutoff = now - timedelta(days=7)
    month_cutoff = now - timedelta(days=30)

    try:
        with connections["analytics"].cursor() as cursor:
            cursor.execute(
                """
                SELECT category, sentiment, scraped_at
                FROM news_articles
                WHERE scraped_at >= %s
                ORDER BY scraped_at DESC
                """,
                [month_cutoff],
            )
            rows = [
                {
                    "category": category,
                    "sentiment": sentiment,
                    "scraped_at": scraped_at,
                }
                for category, sentiment, scraped_at in cursor.fetchall()
            ]
    except Exception as exc:
        return {
            "available": False,
            "message": f"analytics database unavailable: {exc}",
            "today": _summarize_rows([]),
            "windows": {
                "week": _summarize_rows([]),
                "month": _summarize_rows([]),
            },
        }

    today_rows = [
        row
        for row in rows
        if timezone.localtime(row["scraped_at"]).date() == today
    ]
    week_rows = [row for row in rows if row["scraped_at"] >= week_cutoff]
    month_rows = rows

    return {
        "available": True,
        "message": "ok",
        "today": _summarize_rows(today_rows),
        "windows": {
            "week": _summarize_rows(week_rows),
            "month": _summarize_rows(month_rows),
        },
    }
