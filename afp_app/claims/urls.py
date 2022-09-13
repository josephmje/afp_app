from django.urls import path

from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),
    # View entered awards
    path("awards", views.list_awards, name="award_list"),
    # Add award
    path("add_award", views.add_award, name="add_award"),
    # Delete award
    path(
        "r'^delete_award/<uuid:uuid>",
        views.delete_award,
        name="delete_award",
    ),
]
