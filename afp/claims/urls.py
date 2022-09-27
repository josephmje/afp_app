from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("awards/add", views.AddAwardView.as_view(), name="add_award"),
    path(
        "awards/<uuid:pk>/edit",
        views.EditAwardView.as_view(),
        name="edit_award",
    ),
    path(
        "awards/<uuid:pk>/delete",
        views.DeleteAwardView.as_view(),
        name="delete_award",
    ),
]

urlpatterns += [
    path("awards", views.award_list, name="award_list"),
]

urlpatterns += [
    path("grantreviews", views.grantreview_list, name="grantreview_list"),
    path("grantreviews/add", views.add_grantreview, name="add_grantreview"),
    path(
        "grantreviews/<uuid:pk>/edit",
        views.edit_grantreview,
        name="edit_grantreview",
    ),
    path(
        "grantreviews/<uuid:pk>/delete",
        views.delete_grantreview,
        name="delete_grantreview",
    ),
]
