from afp_app.accounts import views
from django.urls import path

urlpatterns = [
    path("logout/", views.logoutaccount, name="logoutaccount"),
    path("login/", views.loginaccount, name="loginaccount"),
]
