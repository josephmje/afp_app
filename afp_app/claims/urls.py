from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("awards/", views.AwardListView.as_view(), name="awards"),
    path(
        "awards/<uuid:uid>",
        views.AwardDetailView.as_view(),
        name="award-detail",
    ),
]
