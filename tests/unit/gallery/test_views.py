"""Tests for gallery views."""

import pytest
from django.test import Client
from django.urls import reverse
from unittest.mock import patch

from tests.unit.gallery.factories import CategoryFactory, PhotoFactory


@pytest.mark.django_db
class TestGalleryViews:
    """Tests for gallery views."""

    def setup_method(self):
        """Set up test client and data."""
        self.client = Client()

    def test_gallery_home_view(self):
        """Test the gallery home view."""
        category = CategoryFactory(name="Nature")
        response = self.client.get(reverse("gallery_home"))

        assert response.status_code == 200
        assert "gallery/gallery.html" in [t.name for t in response.templates]
        assert category in response.context["categories"]

    def test_gallery_home_empty(self):
        """Test the gallery home view with no categories."""
        response = self.client.get(reverse("gallery_home"))

        assert response.status_code == 200
        assert len(response.context["categories"]) == 0

    def test_gallery_category_view(self):
        """Test the gallery category view."""
        category = CategoryFactory(name="Landscapes")
        photo1 = PhotoFactory(category=category, title="Photo 1")
        photo2 = PhotoFactory(category=category, title="Photo 2")

        response = self.client.get(
            reverse("gallery_category", args=[category.id])
        )

        assert response.status_code == 200
        assert response.context["category"] == category
        assert photo1 in response.context["photos"]
        assert photo2 in response.context["photos"]

    def test_gallery_category_not_found(self):
        """Test the gallery category view with invalid category ID."""
        with pytest.raises(Exception):
            self.client.get(reverse("gallery_category", args=[999]))

    def test_hobbies_view(self):
        """Test the hobbies view."""
        dashboard = {
            "available": True,
            "message": "ok",
            "today": {
                "overall": {
                    "label": "POSITIVE",
                    "average_score": 0.4,
                    "article_count": 5,
                },
                "categories": [
                    {
                        "category": "SPORT",
                        "label": "POSITIVE",
                        "average_score": 1.0,
                        "article_count": 3,
                    }
                ],
            },
            "windows": {
                "week": {
                    "overall": {
                        "label": "NEUTRAL",
                        "average_score": 0.1,
                        "article_count": 20,
                    },
                    "categories": [],
                },
                "month": {
                    "overall": {
                        "label": "NEUTRAL",
                        "average_score": 0.0,
                        "article_count": 60,
                    },
                    "categories": [],
                },
            },
        }

        with patch(
            "gallery.views.get_sentiment_dashboard_data",
            return_value=dashboard,
        ):
            response = self.client.get(reverse("hobbies"))

        assert response.status_code == 200
        assert "gallery/hobbies.html" in [t.name for t in response.templates]
        assert (
            response.context["sentiment_dashboard"]["today"]["overall"][
                "label"
            ]
            == "POSITIVE"
        )

    def test_news_sentiment_api(self):
        """Test the news sentiment JSON endpoint."""
        dashboard = {
            "available": True,
            "message": "ok",
            "today": {
                "overall": {
                    "label": "POSITIVE",
                    "average_score": 0.5,
                    "article_count": 4,
                },
                "categories": [],
            },
            "windows": {
                "week": {
                    "overall": {
                        "label": "NEUTRAL",
                        "average_score": 0.0,
                        "article_count": 10,
                    },
                    "categories": [],
                },
                "month": {
                    "overall": {
                        "label": "NEUTRAL",
                        "average_score": 0.0,
                        "article_count": 40,
                    },
                    "categories": [],
                },
            },
        }

        with patch(
            "gallery.views.get_sentiment_dashboard_data",
            return_value=dashboard,
        ):
            response = self.client.get(reverse("news_sentiment_api"))

        assert response.status_code == 200
        assert response.json()["today"]["overall"]["label"] == "POSITIVE"

    def test_homepage_view(self):
        """Test the homepage view."""
        response = self.client.get(reverse("homepage"))

        assert response.status_code == 200
        assert "gallery/homepage.html" in [t.name for t in response.templates]

    def test_personal_view(self):
        """Test the personal view."""
        response = self.client.get(reverse("personal"))

        assert response.status_code == 200
        assert "gallery/personal.html" in [t.name for t in response.templates]
