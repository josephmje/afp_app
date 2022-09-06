from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("award/", views.AwardListView.as_view(), name="awards"),
    path("award/add/", views.create_award, name="create_award"),
    path("award/<str:pk>/", views.update_award, name="update_award"),
    path("award/delete/<str:pk>/", views.delete_award, name="delete_award"),
]
