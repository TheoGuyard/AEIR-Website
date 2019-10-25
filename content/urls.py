from . import views
from django.urls import path

urlpatterns = [
    path('', views.FrontpageView.as_view(), name='frontpage'),
    path('news', views.NewsView.as_view(), name='news'),
    path('team', views.TeamView.as_view(), name='team'),
    path('clubs', views.ClubsView.as_view(), name='clubs'),
    path('events', views.EventsView.as_view(), name='events'),
    path('partners', views.PartnersView.as_view(), name='partners'),
    path('adhesion', views.AdhesionView.as_view(), name='adhesion'),
    path('adhesion_form', views.AdhesionFormView.as_view(), name='adhesion_form'),
    path('adhesion_success', views.AdhesionSuccessView.as_view(), name='adhesion_success'),
]

