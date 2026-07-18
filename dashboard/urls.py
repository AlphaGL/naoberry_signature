from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(
        template_name="dashboard/login.html",
        redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("settings/", views.site_settings, name="settings"),
    path("<str:section>/", views.section_list, name="list"),
    path("<str:section>/add/", views.section_add, name="add"),
    path("<str:section>/<int:pk>/edit/", views.section_edit, name="edit"),
    path("<str:section>/<int:pk>/delete/", views.section_delete, name="delete"),
    path("<str:section>/<int:pk>/toggle/", views.section_toggle, name="toggle"),
]
