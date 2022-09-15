from django.urls import path

from . import views

urlpatterns = [path("", views.home, name="home")]

urlpatterns += [
    path("awards", views.award_list, name="award_list"),
    path("awards/add", views.add_award, name="add_award"),
    path("awards/<int:pk>/edit", views.edit_award, name="edit_award"),
    path("awards/<int:pk>/delete", views.delete_award, name="delete_award"),
]
