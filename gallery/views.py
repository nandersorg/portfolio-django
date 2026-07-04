from django.http import JsonResponse
from django.shortcuts import render
from .models import Category, Photo
from .sentiment import get_sentiment_dashboard_data


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


def hobbies(request):
    return render(
        request,
        "gallery/hobbies.html",
        {"sentiment_dashboard": get_sentiment_dashboard_data()},
    )


def news_sentiment_api(request):
    return JsonResponse(get_sentiment_dashboard_data())


def homepage(request):
    return render(request, "gallery/homepage.html")


def personal(request):
    return render(request, "gallery/personal.html")


def professional(request):
    return render(request, "gallery/professional.html")
