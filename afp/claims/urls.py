from django.urls import path

from . import views

urlpatterns = [path("", views.home, name="home")]

urlpatterns += [
    path("awards", views.award_list, name="award_list"),
    path("awards/add", views.add_award, name="add_award"),
    path("awards/<uuid:pk>/edit", views.edit_award, name="edit_award"),
    path("awards/<uuid:pk>/delete", views.delete_award, name="delete_award"),
]

urlpatterns += [
    path("grantreviews", views.grantreview_list, name="grantreview_list"),
    path("grantreviews/add", views.add_grantreview, name="add_grantreview"),
    path("grantreviews/<uuid:pk>/edit", views.edit_grantreview, name="edit_grantreview"),
    path("grantreviews/<uuid:pk>/delete", views.delete_grantreview, name="delete_grantreview"),
]
