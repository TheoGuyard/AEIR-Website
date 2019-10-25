from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from adhesion.models import Adhesion
from adhesion.forms import AdhesionForm

# Create your views here.

class FrontpageView(TemplateView):
    template_name = 'content/frontpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Page d'accueil"
        context['page_subtitle'] = "L'Association des Élèves de l'INSA Rennes"
        return context

class NewsView(TemplateView):
    template_name = 'content/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Actualités"
        context['page_subtitle'] = "Toutes les news de l'AEIR"
        return context

class TeamView(TemplateView):
    template_name = 'content/team.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Le bureau de l'AEIR"
        context['page_subtitle'] = "Le bureau est composé de 11 membre et est renouvelé chaque année"
        return context

class ClubsView(TemplateView):
    template_name = 'content/clubs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Clubs"
        context['page_subtitle'] = "L'AEIR, c'est plus de 30 clubs"
        return context

class EventsView(TemplateView):
    template_name = 'content/events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Événements"
        context['page_subtitle'] = "Tous les futurs événements de l'AEIR"
        return context

class PartnersView(TemplateView):
    template_name = 'content/partners.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Partenariats"
        context['page_subtitle'] = "Nos partenaires nous accompagnent tout au long de l'année"
        return context

class AdhesionView(TemplateView):
    template_name = 'content/adhesion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Adhésion"
        context['page_subtitle'] = "Pour devenir Amicaliste, c'est par ici !"
        return context

class AdhesionFormView(FormView):
    template_name = 'content/adhesion_form.html'
    form_class = AdhesionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Adhésion"
        context['page_subtitle'] = "Pour devenir Amicaliste, c'est par ici !"
        return context

    def get_success_url(self):
        return redirect('adhesion_success')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class AdhesionSuccessView(TemplateView):
    template_name = 'content/adhesion_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Adhésion"
        context['page_subtitle'] = "Adhésion en cours de traitement"
        return context