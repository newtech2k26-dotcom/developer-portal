from django.urls import path

from . import views

urlpatterns = [

    path("login/", views.user_login, name="login"),

    path("logout/", views.user_logout, name="logout"),

    path("", views.hello, name="hello"),

    path("search/", views.search_developer, name="search_developer"),

    path("guess-number/", views.guess_number, name="guess_number"),

    path("password-analyzer/", views.password_analyzer, name="password_analyzer"),

]