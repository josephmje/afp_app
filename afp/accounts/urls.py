from django.contrib.auth import views as auth_views
from django.urls import path

from afp.accounts.views import user_update_view

app_name = "accounts"

urlpatterns = [
    path("profile", view=user_update_view, name="edit_profile"),
    path(
        "password",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html"
        ),
    ),
]
