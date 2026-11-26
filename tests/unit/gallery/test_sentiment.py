"""Tests for sentiment dashboard data access."""

from unittest.mock import MagicMock, patch

import pytest
from django.db import DatabaseError

from gallery.sentiment import get_sentiment_dashboard_data


def _mock_connections(error):
    connections = MagicMock()
    connections.databases = {"analytics": {}}
    connections["analytics"].cursor.side_effect = error
    return connections


def test_database_error_returns_unavailable_dashboard():
    with patch(
        "gallery.sentiment.connections",
        _mock_connections(DatabaseError("database unavailable")),
    ):
        result = get_sentiment_dashboard_data()

    assert result["available"] is False
    assert result["message"] == (
        "analytics database unavailable: database unavailable"
    )


def test_non_database_error_is_not_suppressed():
    with patch(
        "gallery.sentiment.connections",
        _mock_connections(ValueError("unexpected failure")),
    ), pytest.raises(ValueError, match="unexpected failure"):
        get_sentiment_dashboard_data()
