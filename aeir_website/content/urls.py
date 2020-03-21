from . import views
from django.urls import path

urlpatterns = [
    path("", views.FrontpageView.as_view(), name="frontpage"),
    path("news", views.NewsView.as_view(), name="news"),
    path(
        "news_content_detail/<int:id>",
        views.NewsContentDetailView.as_view(),
        name="news_content_detail",
    ),
    path("team", views.TeamView.as_view(), name="team"),
    path("clubs", views.ClubsView.as_view(), name="clubs"),
    path(
        "club_content_detail/<int:id>",
        views.ClubContentDetailView.as_view(),
        name="club_content_detail",
    ),
    path("event", views.EventView.as_view(), name="event"),
    path(
        "event_content_detail/<int:id>",
        views.EventContentDetailView.as_view(),
        name="event_content_detail",
    ),
    path("partners", views.PartnersView.as_view(), name="partners"),
    path(
        "partner_content_detail/<int:id>",
        views.PartnerContentDetailView.as_view(),
        name="partner_content_detail",
    ),
    path("adhesion", views.AdhesionView.as_view(), name="adhesion"),
    path("adhesion_form", views.AdhesionFormView.as_view(), name="adhesion_form"),
    path(
        "adhesion_success/<uuid:uuid>", views.AdhesionSuccessView.as_view(), name="adhesion_success"
    ),
    path(
        "adhesion_modification_success", views.AdhesionModificationSuccessView.as_view(), name="adhesion_modification_success"
    ),
    path(
        "adhesion_get_card",
        views.AdhesionGetCardView.as_view(),
        name="adhesion_get_card",
    ),
    path(
        "adhesion_not_found",
        views.AdhesionNotFoundView.as_view(),
        name="adhesion_not_found",
    ),
    path(
        "adhesion_need_modifications/<int:id>",
        views.AdhesionNeedModificationView.as_view(),
        name="adhesion_need_modification",
    ),
    path(
        "adhesion_not_paid",
        views.AdhesionNotPaidView.as_view(),
        name="adhesion_not_paid",
    ),
]
