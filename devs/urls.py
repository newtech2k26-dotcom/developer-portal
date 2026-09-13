from django.urls import path
from . import views

urlpatterns = [
    path("", views.hello, name="hello"),
    path("search/", views.search_developer, name="search_developer"),
    path("guess-number/", views.guess_number, name="guess_number"),
]