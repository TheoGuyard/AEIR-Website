from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.http import HttpResponse
from adhesion.models import Adhesion
from adhesion.forms import AdhesionForm
from .models import *
from content.models import GlobalWebsiteParameters

# Create your views here.


class FrontpageView(TemplateView):
    template_name = "content/frontpage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Page d'accueil"
        context["page_subtitle"] = "L'Association des Élèves de l'INSA Rennes"
        context["global_parameters"] = GlobalWebsiteParameters.objects.all().first()
        return context


class NewsView(ListView):
    template_name = "content/news.html"
    model = News
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Actualités"
        context["page_subtitle"] = "Toutes les news de l'AEIR sont ici !"
        return context

    def get_queryset(self):
        return News.objects.all().order_by("-date")


class NewsContentDetailView(DetailView):
    template_name = "content/news_content_detail.html"
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Actualités"
        context["page_subtitle"] = "Toutes les news de l'AEIR sont ici !"
        return context

    def get_object(self, queryset=None):
        obj = News.objects.get(id=self.kwargs["id"])
        return obj


class TeamView(ListView):
    template_name = "content/team.html"
    model = TeamMember

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Le bureau de l'AEIR"
        context[
            "page_subtitle"
        ] = "Le bureau est composé de membre surmotivés et est renouvelé chaque année"
        return context

    def get_queryset(self):
        return TeamMember.objects.all()


class ClubsView(ListView):
    template_name = "content/clubs.html"
    model = Club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Clubs"
        context["page_subtitle"] = "L'AEIR, c'est plus de 30 clubs"
        return context

class ClubContentDetailView(DetailView):
    template_name = "content/club_content_detail.html"
    model = Club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Clubs"
        context["page_subtitle"] = "L'AEIR, c'est plus de 30 clubs"
        return context

    def get_object(self, queryset=None):
        obj = Club.objects.get(id=self.kwargs["id"])
        return obj

class EventView(ListView):
    template_name = "content/event.html"
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Événements"
        context["page_subtitle"] = "Tous les futurs événements de l'AEIR"
        return context


class EventContentDetailView(DetailView):
    template_name = "content/event_content_detail.html"
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Actualités"
        context["page_subtitle"] = "Tous les futurs événements de l'AEIR"
        return context

    def get_object(self, queryset=None):
        obj = Event.objects.get(id=self.kwargs["id"])
        return obj


class PartnersView(ListView):
    template_name = "content/partners.html"
    model = Partner
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Partenariats"
        context[
            "page_subtitle"
        ] = "Nos partenaires nous accompagnent tout au long de l'année"
        return context


class PartnerContentDetailView(DetailView):
    template_name = "content/partner_content_detail.html"
    model = Partner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Partenariats"
        context[
            "page_subtitle"
        ] = "Nos partenaires nous accompagnent tout au long de l'année"
        return context

    def get_object(self, queryset=None):
        obj = Partner.objects.get(id=self.kwargs["id"])
        return obj


class AdhesionView(TemplateView):
    template_name = "content/adhesion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Adhésion"
        context["page_subtitle"] = "Pour devenir Amicaliste, c'est par ici !"
        context["global_parameters"] = GlobalWebsiteParameters.objects.all().first()
        return context


class AdhesionFormView(CreateView):
    template_name = 'content/adhesion_form.html'
    form_class = AdhesionForm
    success_url = 'adhesion_success'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Adhésion"
        context["page_subtitle"] = "Pour devenir Amicaliste, c'est par ici !"
        context["cgv"] = GlobalWebsiteParameters.objects.first().conditions_adhesion.url
        return context

class AdhesionSuccessView(TemplateView):
    template_name = "content/adhesion_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Adhésion"
        context["page_subtitle"] = "Adhésion en cours de traitement"
        adhesion = Adhesion.objects.filter(paid='False').order_by('-adhesion_date').first()
        context["adhesion"] = adhesion
        return context


class AdhesionGetCardView(TemplateView):
    template_name = "content/adhesion_get_card.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Adhésion"
        context["page_subtitle"] = "Récupération d'une carte Amicaliste"
        return context

    def post(self, request):
        form = request.POST
        print(form)
        try:
            user = Adhesion.objects.get(
                card_id=form["username"], card_pwd=form["password"]
            )
        except:
            user = None
        if not user:
            return redirect("adhesion_not_found")
        else:
            if not user.valid_infos:
                return redirect("adhesion_need_modification", id=user.id)
            elif user.valid_infos and not user.paid:
                return redirect("adhesion_not_paid")
            else:
                return user.card


class AdhesionNotFoundView(TemplateView):
    template_name = "content/adhesion_not_found.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Adhésion"
        context["page_subtitle"] = "Adhésion non trouvée"
        return context


class AdhesionNeedModificationView(UpdateView):

    template_name = "content/adhesion_need_modification.html"
    model = Adhesion
    form_class = AdhesionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Adhésion"
        context["page_subtitle"] = "Adhésion non trouvée"
        return context

    def get_success_url(self):
        return redirect("adhesion_success")

    def get_object(self, queryset=None):
        obj = Adhesion.objects.get(id=self.kwargs["id"])
        return obj


class AdhesionNotPaidView(TemplateView):

    template_name = "content/adhesion_not_paid.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Adhésion"
        context["page_subtitle"] = "Adhésion non payée"
        return context