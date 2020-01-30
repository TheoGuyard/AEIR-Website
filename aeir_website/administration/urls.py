from . import views
from django.urls import path

urlpatterns = [
    ### Connexion ###
    path("", views.AdministrationView.as_view(), name="administration"),
    path("login", views.AdministrationLoginView.as_view(), name="login"),
    path("logout", views.AdministrationLogoutView.as_view(), name="logout"),
    path(
        "permission_denied",
        views.AdministrationPermissionDeniedView.as_view(),
        name="permission_denied",
    ),
    path(
        "admin_error", views.AdministrationAdminErrorView.as_view(), name="admin_error"
    ),
    ### Adhésions ###
    path(
        "adherent_list",
        views.AdministrationAdherentListView.as_view(),
        name="adherent_list",
    ),
    path(
        "adherent_update/<int:id>",
        views.AdministrationAdherentUpdateView.as_view(),
        name="adherent_update",
    ),
    path(
        "adherent_delete/<int:id>",
        views.AdministrationAdherentDeleteView.as_view(),
        name="adherent_delete",
    ),
    path(
        "new_adherent_list",
        views.AdministrationNewAdherentListView.as_view(),
        name="new_adherent_list",
    ),
    path(
        "new_adherent_detail/<int:pk>",
        views.AdministrationNewAdherentDetailView.as_view(),
        name="new_adherent_detail",
    ),
    path(
        "new_adherent_delete/<int:id>",
        views.AdministrationNewAdherentDeleteView.as_view(),
        name="new_adherent_delete",
    ),
    path(
        "adherent_search",
        views.AdministrationAdherentSearchView.as_view(),
        name="adherent_search",
    ),
    ### Content ###
    # Global parameters
    path(
        "global_parameters_update",
        views.AdministrationGlobalParametersUpdateView.as_view(),
        name="global_parameters_update",
    ),
    # News
    path("news_list", views.AdministrationNewsListView.as_view(), name="news_list"),
    path(
        "news_detail/<int:pk>",
        views.AdministrationNewsDetailView.as_view(),
        name="news_detail",
    ),
    path(
        "news_create", views.AdministrationNewsCreateView.as_view(), name="news_create"
    ),
    path(
        "news_update/<int:pk>",
        views.AdministrationNewsUpdateView.as_view(),
        name="news_update",
    ),
    path(
        "news_delete/<int:id>",
        views.AdministrationNewsDeleteView.as_view(),
        name="news_delete",
    ),
    # Team
    path("team_list", views.AdministrationTeamListView.as_view(), name="team_list"),
    path(
        "team_detail/<int:pk>",
        views.AdministrationTeamDetailView.as_view(),
        name="team_detail",
    ),
    path(
        "team_create", views.AdministrationTeamCreateView.as_view(), name="team_create"
    ),
    path(
        "team_update/<int:pk>",
        views.AdministrationTeamUpdateView.as_view(),
        name="team_update",
    ),
    path(
        "team_delete/<int:id>",
        views.AdministrationTeamDeleteView.as_view(),
        name="team_delete",
    ),
    # Partner
    path(
        "partner_list",
        views.AdministrationPartnerListView.as_view(),
        name="partner_list",
    ),
    path(
        "partner_detail/<int:pk>",
        views.AdministrationPartnerDetailView.as_view(),
        name="partner_detail",
    ),
    path(
        "partner_create",
        views.AdministrationPartnerCreateView.as_view(),
        name="partner_create",
    ),
    path(
        "partner_update/<int:pk>",
        views.AdministrationPartnerUpdateView.as_view(),
        name="partner_update",
    ),
    path(
        "partner_delete/<int:id>",
        views.AdministrationPartnerDeleteView.as_view(),
        name="partner_delete",
    ),
    # Event
    path("event_list", views.AdministrationEventListView.as_view(), name="event_list"),
    path(
        "event_detail/<int:pk>",
        views.AdministrationEventDetailView.as_view(),
        name="event_detail",
    ),
    path(
        "event_create",
        views.AdministrationEventCreateView.as_view(),
        name="event_create",
    ),
    path(
        "event_update/<int:pk>",
        views.AdministrationEventUpdateView.as_view(),
        name="event_update",
    ),
    path(
        "event_delete/<int:id>",
        views.AdministrationEventDeleteView.as_view(),
        name="event_delete",
    ),
    ### Clubs ###
    # Clubs
    path("club_list", views.AdministrationClubListView.as_view(), name="club_list"),
    path(
        "club_detail/<int:pk>",
        views.AdministrationClubDetailView.as_view(),
        name="club_detail",
    ),
    path(
        "club_create", views.AdministrationClubCreateView.as_view(), name="club_create"
    ),
    path(
        "club_update/<int:pk>",
        views.AdministrationClubUpdateView.as_view(),
        name="club_update",
    ),
    path(
        "club_delete/<int:id>",
        views.AdministrationClubDeleteView.as_view(),
        name="club_delete",
    ),
    # Evenements
    path(
        "event_management_list",
        views.AdministrationEventManagementListView.as_view(),
        name="event_management_list",
    ),
    path(
        "event_management_create",
        views.AdministrationEventManagementCreateView.as_view(),
        name="event_management_create",
    ),
    path(
        "event_management_participants/<int:pk>",
        views.AdministrationEventManagementParticipantsView.as_view(),
        name="event_management_participants",
    ),
    path(
        "event_management_prevente/<int:pk>",
        views.AdministrationEventManagementPreventeView.as_view(),
        name="event_management_prevente",
    ),
    path(
        "event_management_delete/<int:pk>",
        views.AdministrationEventManagementDeleteView.as_view(),
        name="event_management_delete",
    ),
    ### Changement d'année ###
    path(
        "archived_adherent_search",
        views.AdministrationArchivedAdhesionSearchView.as_view(),
        name="archived_adherent_search",
    ),
    path(
        "archived_adherent_delete/<int:id>",
        views.AdministrationArchivedAdherentDeleteView.as_view(),
        name="archived_adherent_delete",
    ),
    path(
        "import_adhesion",
        views.AdministrationImportAdhesionView.as_view(),
        name="import_adhesion",
    ),
    path(
        "change_year", views.AdministrationChangeYearView.as_view(), name="change_year"
    ),
]
