from django.urls import path

from . import views

urlpatterns = [

    path("login/", views.user_login, name="login"),

    path("logout/", views.user_logout, name="logout"),

    path("home/", views.hello, name="hello"),

    path("search/", views.search_developer, name="search_developer"),

    path("guess-number/", views.guess_number, name="guess_number"),

    path("password-analyzer/", views.password_analyzer, name="password_analyzer"),

    # =====================================================
    # Menu Management
    # =====================================================

    path("menu-management/", views.menu_management, name="menu_management"),

    path("menu-management/create/", views.menu_create, name="menu_create"),

    path("menu-management/edit/<int:menu_id>/", views.menu_edit, name="menu_edit"),

    path("menu-management/delete/<int:menu_id>/", views.menu_delete, name="menu_delete"),
]