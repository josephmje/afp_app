from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path(
        "profile",
        views.ProfileUpdateView.as_view(),
        name="edit_profile",
    ),
    path(
        "password",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html"
        ),
    ),
]
