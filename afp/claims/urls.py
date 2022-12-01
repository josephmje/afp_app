from django.urls import path

from . import views

urlpatterns = [path("", views.HomeView.as_view(), name="home")]

urlpatterns += [
    path("awards", views.AwardListView.as_view(), name="award_list"),
    path("awards/add", views.AwardCreateView.as_view(), name="add_award"),
    path(
        "awards/<uuid:pk>/edit",
        views.AwardUpdateView.as_view(),
        name="edit_award",
    ),
    path(
        "awards/<uuid:pk>/delete",
        views.AwardDeleteView.as_view(),
        name="delete_award",
    ),
]

urlpatterns += [
    path(
        "promotions", views.PromotionListView.as_view(), name="promotion_list"
    ),
    path(
        "promotions/add",
        views.PromotionCreateView.as_view(),
        name="add_promotion",
    ),
    path(
        "promotions/<uuid:pk>/edit",
        views.PromotionUpdateView.as_view(),
        name="edit_promotion",
    ),
    path(
        "promotions/<uuid:pk>/delete",
        views.PromotionDeleteView.as_view(),
        name="delete_promotion",
    ),
]

urlpatterns += [
    path(
        "publications",
        views.PublicationListView.as_view(),
        name="publication_list",
    ),
    path(
        "publications/add",
        views.PublicationCreateView.as_view(),
        name="add_publication",
    ),
    path(
        "publications/<uuid:pk>/edit",
        views.PublicationUpdateView.as_view(),
        name="edit_publication",
    ),
    path(
        "publications/<uuid:pk>/delete",
        views.PublicationDeleteView.as_view(),
        name="delete_publication",
    ),
]

urlpatterns += [
    path(
        "editorial_boards",
        views.EditorialBoardListView.as_view(),
        name="editorial_board_list",
    ),
    path(
        "editorial_boards/add",
        views.EditorialBoardCreateView.as_view(),
        name="add_editorial_board",
    ),
    path(
        "editorial_boards/<uuid:pk>/edit",
        views.EditorialBoardUpdateView.as_view(),
        name="edit_editorial_board",
    ),
    path(
        "editorial_boards/<uuid:pk>/delete",
        views.EditorialBoardDeleteView.as_view(),
        name="delete_editorial_board",
    ),
]

urlpatterns += [
    path(
        "grants",
        views.GrantListView.as_view(),
        name="grant_list",
    ),
    path(
        "grants/add",
        views.GrantCreateView.as_view(),
        name="add_grant",
    ),
    path(
        "grants/<uuid:pk>/edit",
        views.GrantUpdateView.as_view(),
        name="edit_grant",
    ),
    path(
        "grants/<uuid:pk>/delete",
        views.GrantDeleteView.as_view(),
        name="delete_grant",
    ),
    path(
        "grant_link/<uuid:pk>/delete",
        views.GrantLinkDeleteView.as_view(),
        name="delete_grantlink",
    ),
]

urlpatterns += [
    path(
        "grantreviews",
        views.GrantReviewListView.as_view(),
        name="grantreview_list",
    ),
    path(
        "grantreviews/add",
        views.GrantReviewCreateView.as_view(),
        name="add_grantreview",
    ),
    path(
        "grantreviews/<uuid:pk>/edit",
        views.GrantReviewUpdateView.as_view(),
        name="edit_grantreview",
    ),
    path(
        "grantreviews/<uuid:pk>/delete",
        views.GrantReviewDeleteView.as_view(),
        name="delete_grantreview",
    ),
]

urlpatterns += [
    path(
        "committees", views.CommitteeListView.as_view(), name="committee_list"
    ),
    path(
        "committees/add",
        views.CommitteeCreateView.as_view(),
        name="add_committee",
    ),
    path(
        "committees/<uuid:pk>/edit",
        views.CommitteeUpdateView.as_view(),
        name="edit_committee",
    ),
    path(
        "committees/<uuid:pk>/delete",
        views.CommitteeDeleteView.as_view(),
        name="delete_committee",
    ),
]

urlpatterns += [
    path("lectures", views.LectureListView.as_view(), name="lecture_list"),
    path(
        "lectures/add", views.LectureCreateView.as_view(), name="add_lecture"
    ),
    path(
        "lectures/<uuid:pk>/edit",
        views.LectureUpdateView.as_view(),
        name="edit_lecture",
    ),
    path(
        "lectures/<uuid:pk>/delete",
        views.LectureDeleteView.as_view(),
        name="delete_lecture",
    ),
]

urlpatterns += [
    path("exams", views.ExamListView.as_view(), name="exam_list"),
    path("exams/add", views.ExamCreateView.as_view(), name="add_exam"),
    path(
        "exams/<uuid:pk>/edit",
        views.ExamUpdateView.as_view(),
        name="edit_exam",
    ),
    path(
        "exams/<uuid:pk>/delete",
        views.ExamDeleteView.as_view(),
        name="delete_exam",
    ),
]

urlpatterns += [
    path(
        "supervision",
        views.SupervisionListView.as_view(),
        name="supervision_list",
    ),
    path(
        "supervision/add",
        views.SupervisionCreateView.as_view(),
        name="add_supervision",
    ),
    path(
        "supervision/<uuid:pk>/edit",
        views.SupervisionUpdateView.as_view(),
        name="edit_supervision",
    ),
    path(
        "supervision/<uuid:pk>/delete",
        views.SupervisionDeleteView.as_view(),
        name="delete_supervision",
    ),
]

urlpatterns += [
    path("cpa", views.CpaListView.as_view(), name="cpa_list"),
    path("cpa/add", views.CpaCreateView.as_view(), name="add_cpa"),
    path(
        "cpa/<uuid:pk>/edit",
        views.CpaUpdateView.as_view(),
        name="edit_cpa",
    ),
    path(
        "cpa/<uuid:pk>/delete",
        views.CpaDeleteView.as_view(),
        name="delete_cpa",
    ),
]
