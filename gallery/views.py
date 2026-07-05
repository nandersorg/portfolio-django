import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Category, Photo
from .sentiment import get_sentiment_dashboard_data

QUICKDRAW_PREDICT_URL = os.getenv(
    "QUICKDRAW_PREDICT_URL",
    (
        "http://127.0.0.1:31548/predict"
        if os.getenv("DEBUG", "False") == "True"
        else (
            "http://quickdraw-serving.ml-serving.svc.cluster.local:"
            "8000/predict"
        )
    ),
)


def _is_valid_quickdraw_image(image):
    if not isinstance(image, list) or len(image) != 28:
        return False

    for row in image:
        if not isinstance(row, list) or len(row) != 28:
            return False
        if not all(isinstance(pixel, (int, float)) for pixel in row):
            return False

    return True


def _predict_quickdraw(image):
    payload = json.dumps({"image": image}).encode("utf-8")
    request = Request(
        QUICKDRAW_PREDICT_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def gallery_home(request):
    categories = Category.objects.all()
    return render(request, "gallery/gallery.html", {"categories": categories})


def gallery_category(request, category_id):
    category = Category.objects.get(id=category_id)
    photos = Photo.objects.filter(category=category)
    return render(
        request,
        "gallery/gallery-category.html",
        {"category": category, "photos": photos},
    )


@ensure_csrf_cookie
def hobbies(request):
    return render(
        request,
        "gallery/hobbies.html",
        {
            "sentiment_dashboard": get_sentiment_dashboard_data(),
            "quickdraw_predict_url": "/api/quickdraw-predict/",
        },
    )


def news_sentiment_api(request):
    return JsonResponse(get_sentiment_dashboard_data())


def quickdraw_predict_api(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed."},
            status=405,
        )

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    image = payload.get("image")
    if not _is_valid_quickdraw_image(image):
        return JsonResponse(
            {"error": "Image must be a 28x28 matrix of numbers."},
            status=400,
        )

    try:
        prediction = _predict_quickdraw(image)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return JsonResponse(
            {
                "error": "QuickDraw service returned an error.",
                "detail": detail,
            },
            status=502,
        )
    except URLError as exc:
        return JsonResponse(
            {
                "error": "QuickDraw service is unavailable.",
                "detail": str(exc.reason),
            },
            status=502,
        )
    except (TimeoutError, ValueError, json.JSONDecodeError):
        return JsonResponse(
            {"error": "QuickDraw service returned an invalid response."},
            status=502,
        )

    if "prediction" not in prediction:
        return JsonResponse(
            {"error": "QuickDraw service returned an invalid response."},
            status=502,
        )

    return JsonResponse({"prediction": prediction["prediction"]})


def homepage(request):
    return render(request, "gallery/homepage.html")


def personal(request):
    return render(request, "gallery/personal.html")


def professional(request):
    return render(request, "gallery/professional.html")
