from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from adhesion.models import Adhesion, ArchivedAdhesion
from adhesion.forms import AdhesionForm
from content.models import *
from content.forms import *
from .csv_extract import list_to_csv, list_to_csv_event
from .forms import AdhesionFilter, EventManagementForm, ArchivedAdhesionFilter
from .models import *
from zipfile import ZipFile
from bs4 import BeautifulSoup

### Connexion ###


class AdministrationLoginView(LoginView):
    template_name = "administration/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Login"
        context["page_subtitle"] = "Identifez vous pour administrer le site"
        return context


class AdministrationLogoutView(LoginRequiredMixin, LogoutView):
    login_url = "login"
    template_name = "administration/logout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Logout"
        context["page_subtitle"] = "À plus mon ptit !"
        return context


class AdministrationPermissionDeniedView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "administration/permission_denied.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Accès refusé"
        return context


class AdministrationView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    redirect_field_name = ""
    template_name = "administration/administration.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = (
            "Bienvenue dans le panneau d'administration !"
        )
        return context


class AdministrationAdminErrorView(LoginView):
    template_name = "administration/admin_error.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Erreur"
        return context


### Adhésions ###


class AdministrationAdherentListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "administration/adherent_list.html"
    model = Adhesion
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des adhésions"
        context["number"] = len(self.get_queryset())
        return context

    def get_queryset(self):
        return Adhesion.objects.filter(paid=True).order_by("first_name")

    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")

    def post(self, request):
        form = request.POST
        if "card" in form:
            user = Adhesion.objects.get(id=int(form["card"]))
            return user.card
        elif "csv" in form:
            return list_to_csv(Adhesion.objects.filter(paid=True))
        else:
            redirect("")


class AdministrationAdherentUpdateView(
    UserPassesTestMixin, LoginRequiredMixin, UpdateView
):
    login_url = "login"
    template_name = "administration/adherent_update.html"
    model = Adhesion
    form_class = AdhesionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des adhésions"
        return context

    def get_success_url(self):
        return reverse("administration")

    def get_object(self, queryset=None):
        obj = Adhesion.objects.get(id=self.kwargs["id"])
        return obj

    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationAdherentDeleteView(
    UserPassesTestMixin, LoginRequiredMixin, DeleteView
):
    login_url = "login"
    template_name = "administration/adherent_delete.html"
    model = Adhesion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des adhésions"
        return context

    def get_object(self, queryset=None):
        obj = Adhesion.objects.get(id=self.kwargs["id"])
        return obj

    def get_success_url(self):
        return reverse("adherent_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")

class AdministrationNewAdherentDeleteView(
    UserPassesTestMixin, LoginRequiredMixin, DeleteView
):
    login_url = "login"
    template_name = "administration/new_adherent_delete.html"
    model = Adhesion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des adhésions"
        return context

    def get_object(self, queryset=None):
        obj = Adhesion.objects.get(id=self.kwargs["id"])
        return obj

    def get_success_url(self):
        return reverse("new_adherent_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationNewAdherentListView(
    UserPassesTestMixin, LoginRequiredMixin, ListView
):
    login_url = "login"
    template_name = "administration/new_adherent_list.html"
    model = Adhesion
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des adhésions"
        context["number"] = len(self.get_queryset())
        return context

    def get_queryset(self):
        return Adhesion.objects.filter(paid=False).order_by("first_name")

    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")

    def post(self, request):
        form = request.POST
        print(form)
        if "card" in form:
            user = Adhesion.objects.get(id=int(form["card"]))
            return user.card
        return HttpResponseRedirect("")


class AdministrationNewAdherentDetailView(
    UserPassesTestMixin, LoginRequiredMixin, DetailView
):
    login_url = "login"
    template_name = "administration/new_adherent_detail.html"
    model = Adhesion

    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")

    def post(self, request, pk):
        form = request.POST
        adherent = Adhesion.objects.get(pk=self.kwargs["pk"])
        if "need_modification" in form.keys():
            adherent.valid_infos = False
            adherent.save()
        elif "validate" in form.keys():
            adherent.valid_infos = True
            adherent.paid = True
            adherent.save()
        else:
            return redirect("admin_error")
        return redirect("new_adherent_list")


class AdministrationAdherentSearchView(
    UserPassesTestMixin, LoginRequiredMixin, TemplateView
):
    login_url = "login"
    template_name = "administration/adherent_search.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des adhésions"
        context["filter"] = AdhesionFilter(
            self.request.GET, queryset=Adhesion.objects.filter(paid=True)
        )
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect("administration_no_permission")

    def post(self, request):

        form = request.POST or None
        if "card" in form:
            user = Adhesion.objects.get(id=int(form["card"]))
            return user.card
        return HttpResponseRedirect("")


### Content ###

# Global parameters


class AdministrationGlobalParametersUpdateView(
    UserPassesTestMixin, LoginRequiredMixin, UpdateView
):
    login_url = "login"
    template_name = "administration/global_parameters_update.html"
    model = GlobalWebsiteParameters
    form_class = GlobalWebsiteParametersForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def get_object(self):
        return GlobalWebsiteParameters.objects.all().first()

    def get_success_url(self, *args, **kwargs):
        return reverse("administration")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


# News


class AdministrationNewsListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "administration/news_list.html"
    model = News
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        context["number"] = len(self.get_queryset())
        return context

    def get_queryset(self):
        return News.objects.all().order_by("-date")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationNewsDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    login_url = "login"
    template_name = "administration/news_detail.html"
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationNewsCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "administration/news_create.html"
    model = News
    form_class = NewsForm
    success_url = "news_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationNewsUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    login_url = "login"
    template_name = "administration/news_update.html"
    model = News
    form_class = NewsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse("news_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationNewsDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    login_url = "login"
    template_name = "administration/news_delete.html"
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def get_object(self, queryset=None):
        obj = News.objects.get(id=self.kwargs["id"])
        return obj

    def get_success_url(self):
        return reverse("news_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


# Team


class AdministrationTeamListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "administration/team_list.html"
    model = TeamMember
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        context["number"] = len(self.get_queryset())
        return context

    def get_queryset(self):
        return TeamMember.objects.all()

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationTeamDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    login_url = "login"
    template_name = "administration/team_detail.html"
    model = TeamMember

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationTeamCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "administration/team_create.html"
    model = TeamMember
    form_class = TeamMemberForm
    success_url = "team_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationTeamUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    login_url = "login"
    template_name = "administration/team_update.html"
    model = TeamMember
    form_class = TeamMemberForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse("team_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationTeamDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    login_url = "login"
    template_name = "administration/team_delete.html"
    model = TeamMember

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def get_object(self, queryset=None):
        obj = TeamMember.objects.get(id=self.kwargs["id"])
        return obj

    def get_success_url(self):
        return reverse("team_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


# Event


class AdministrationEventListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "administration/event_list.html"
    model = Event
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        context["number"] = len(self.get_queryset())
        return context

    def get_queryset(self):
        return Event.objects.all().order_by("date")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationEventDetailView(
    UserPassesTestMixin, LoginRequiredMixin, DetailView
):
    login_url = "login"
    template_name = "administration/event_detail.html"
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationEventCreateView(
    UserPassesTestMixin, LoginRequiredMixin, CreateView
):
    login_url = "login"
    template_name = "administration/event_create.html"
    model = Event
    form_class = EventForm
    success_url = "event_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationEventUpdateView(
    UserPassesTestMixin, LoginRequiredMixin, UpdateView
):
    login_url = "login"
    template_name = "administration/event_update.html"
    model = Event
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse("event_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationEventDeleteView(
    UserPassesTestMixin, LoginRequiredMixin, DeleteView
):
    login_url = "login"
    template_name = "administration/event_delete.html"
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def get_object(self, queryset=None):
        obj = Event.objects.get(id=self.kwargs["id"])
        return obj

    def get_success_url(self):
        return reverse("event_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


# Partner


class AdministrationPartnerListView(UserPassesTestMixin, LoginRequiredMixin, ListView):

    login_url = "login"
    template_name = "administration/partner_list.html"
    model = Partner
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        context["number"] = len(self.get_queryset())
        return context

    def get_queryset(self):
        return Partner.objects.all().order_by("name")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationPartnerDetailView(
    UserPassesTestMixin, LoginRequiredMixin, DetailView
):
    login_url = "login"
    template_name = "administration/partner_detail.html"
    model = Partner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationPartnerCreateView(
    UserPassesTestMixin, LoginRequiredMixin, CreateView
):
    login_url = "login"
    template_name = "administration/partner_create.html"
    model = Partner
    form_class = PartnerForm
    success_url = "partner_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationPartnerUpdateView(
    UserPassesTestMixin, LoginRequiredMixin, UpdateView
):
    login_url = "login"
    template_name = "administration/partner_update.html"
    model = Partner
    form_class = PartnerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse("partner_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationPartnerDeleteView(
    UserPassesTestMixin, LoginRequiredMixin, DeleteView
):
    login_url = "login"
    template_name = "administration/partner_delete.html"
    model = Partner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion du contenu"
        return context

    def get_object(self, queryset=None):
        obj = Partner.objects.get(id=self.kwargs["id"])
        return obj

    def get_success_url(self):
        return reverse("partner_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


### Clubs ###

# Club


class AdministrationClubListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "administration/club_list.html"
    model = Club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des clubs"
        context["number"] = len(self.get_queryset())
        return context

    def get_queryset(self):
        return Club.objects.all().order_by("name")

    def test_func(self):
        return (
            self.request.user.groups.filter(name="Club management").exists()
            or self.request.user.groups.filter(name="Content management").exists()
        )

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationClubDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    login_url = "login"
    template_name = "administration/club_detail.html"
    model = Club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des clubs"
        return context

    def test_func(self):
        return (
            self.request.user.groups.filter(name="Club management").exists()
            or self.request.user.groups.filter(name="Content management").exists()
        )

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationClubCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "administration/club_create.html"
    model = Club
    form_class = ClubForm
    success_url = "club_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des clubs"
        return context

    def test_func(self):
        return (
            self.request.user.groups.filter(name="Club management").exists()
            or self.request.user.groups.filter(name="Content management").exists()
        )

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationClubUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    login_url = "login"
    template_name = "administration/club_update.html"
    model = Club
    form_class = ClubForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des clubs"
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse("club_list")

    def test_func(self):
        return (
            self.request.user.groups.filter(name="Club management").exists()
            or self.request.user.groups.filter(name="Content management").exists()
        )

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationClubDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    login_url = "login"
    template_name = "administration/club_delete.html"
    model = Club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des clubs"
        return context

    def get_object(self, queryset=None):
        obj = Club.objects.get(id=self.kwargs["id"])
        return obj

    def get_success_url(self):
        return reverse("club_list")

    def test_func(self):
        return (
            self.request.user.groups.filter(name="Club management").exists()
            or self.request.user.groups.filter(name="Content management").exists()
        )

    def handle_no_permission(self):
        return redirect("permission_denied")


# Préventes


class AdministrationEventManagementListView(
    UserPassesTestMixin, LoginRequiredMixin, ListView
):

    login_url = "login"
    template_name = "administration/event_management_list.html"
    model = EventManagement
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des clubs"
        context["number"] = len(self.get_queryset())
        return context

    def get_queryset(self):
        return EventManagement.objects.all().order_by("date")

    def test_func(self):
        return self.request.user.groups.filter(name="Club management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationEventManagementCreateView(
    UserPassesTestMixin, LoginRequiredMixin, CreateView
):
    login_url = "login"
    template_name = "administration/event_management_create.html"
    model = EventManagement
    form_class = EventManagementForm
    success_url = "event_management_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des clubs"
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Club management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


class AdministrationEventManagementParticipantsView(
    UserPassesTestMixin, LoginRequiredMixin, TemplateView
):

    login_url = "login"
    template_name = "administration/event_management_participants.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des clubs"
        context["event"] = EventManagement.objects.get(pk=self.kwargs["pk"])
        context["participants"] = (
            context["event"].participants.all().order_by("last_name")
        )
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Club management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")

    def post(self, request, pk):

        form = request.POST or None
        event = EventManagement.objects.get(pk=self.kwargs["pk"])
        for button in form:
            if button.startswith("delete_adherent_"):
                user_id = button.split("_")[-1]
                event.participants.remove(Adhesion.objects.get(id=int(user_id)))
                event.save()
            if button.startswith("delete_non_adherent"):
                if event.participants_non_adherents > 0:
                    event.participants_non_adherents -= 1
                else:
                    event.participants_non_adherents = 0
                event.save()
            if button.startswith("csv_extract"):
                return list_to_csv_event(event.participants.all())

        return HttpResponseRedirect("")


class AdministrationEventManagementPreventeView(
    UserPassesTestMixin, LoginRequiredMixin, DetailView
):
    login_url = "login"
    template_name = "administration/event_management_prevente.html"
    model = EventManagement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des clubs"
        event = EventManagement.objects.get(pk=self.kwargs["pk"])
        participants = event.participants.all()
        context["filter"] = AdhesionFilter(
            self.request.GET,
            queryset=Adhesion.objects.filter(paid=True).exclude(pk__in=participants),
        )
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Club management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")

    def post(self, request, pk):

        form = request.POST or None
        event = EventManagement.objects.get(pk=self.kwargs["pk"])
        for button in form:
            if button.startswith("adherent"):
                user_id = form[button].split("_")[-1]
                event.participants.add(Adhesion.objects.get(id=int(user_id)))
                event.save()
            if button.startswith("non_adherent"):
                event.participants_non_adherents += 1
                event.save()

        return HttpResponseRedirect("")


class AdministrationEventManagementDeleteView(
    UserPassesTestMixin, LoginRequiredMixin, DeleteView
):
    login_url = "login"
    template_name = "administration/event_management_delete.html"
    model = EventManagement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Gestion des clubs"
        return context

    def get_object(self, queryset=None):
        obj = EventManagement.objects.get(pk=self.kwargs["pk"])
        return obj

    def get_success_url(self):
        return reverse("event_management_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Club management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")


### Changement d'année ###


class AdministrationArchivedAdhesionSearchView(
    UserPassesTestMixin, LoginRequiredMixin, TemplateView
):
    login_url = "login"
    template_name = "administration/archived_adherent_search.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Changement d'année"
        context["filter"] = ArchivedAdhesionFilter(
            self.request.GET, queryset=ArchivedAdhesion.objects.filter()
        )
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Year management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")

    def post(self, request):

        form = request.POST
        adherent = ArchivedAdhesion.objects.get(id=int(form['send_mail']))
        adherent.send_mail()

        return redirect('archived_adherent_search')

class AdministrationArchivedAdherentDeleteView(
    UserPassesTestMixin, LoginRequiredMixin, DeleteView
):
    login_url = "login"
    template_name = "administration/archived_adherent_delete.html"
    model = ArchivedAdhesion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Changement d'année"
        return context

    def get_object(self, queryset=None):
        obj = ArchivedAdhesion.objects.get(id=self.kwargs["id"])
        return obj

    def get_success_url(self):
        return reverse("archived_adherent_search")

    def test_func(self):
        return self.request.user.groups.filter(name="Year management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")



class AdministrationChangeYearView(
    UserPassesTestMixin, LoginRequiredMixin, TemplateView
):
    login_url = "login"
    template_name = "administration/change_year.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Changement d'année"
        context["filter"] = ArchivedAdhesionFilter(
            self.request.GET, queryset=ArchivedAdhesion.objects.filter()
        )
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Year management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")

    def post(self, request):
        nb_transfer = 0
        nb_fail = 0
        adhesions = Adhesion.objects.filter(paid=True)
        for adhesion in adhesions:
            archived_adhesion = ArchivedAdhesion.objects.create(
                first_name=adhesion.first_name,
                last_name=adhesion.last_name,
                email=adhesion.email,
                insa_student=adhesion.insa_student,
                school_year=adhesion.school_year,
                departement=adhesion.departement,
                adhesion_date=adhesion.adhesion_date,
                year=int(adhesion.year.split(" ")[0]),
            )
            archived_adhesion.save()
            nb_transfer += 1
            # except:
            #    nb_fail += 1
        print(nb_transfer, nb_fail)

        return redirect("administration")


class AdministrationImportAdhesionView(
    UserPassesTestMixin, LoginRequiredMixin, TemplateView
):
    login_url = "login"
    template_name = "administration/import_adhesion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Administration"
        context["page_subtitle"] = "Changement d'année"
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Year management").exists()

    def handle_no_permission(self):
        return redirect("permission_denied")

    def post(self, request):

        # Save file locally
        file = request.FILES["myfile"]
        fs = FileSystemStorage(location="media/import_adhesion")
        filename = fs.save(file.name, file)

        # Unzip
        uploaded_file_url = "media/import_adhesion/" + file.name
        with ZipFile(uploaded_file_url, "r") as zipfile:
            zipfile.extractall("media/import_adhesion/")
            zipfile.close
        fs.delete(filename)

        # Read HTML file
        with open("media/import_adhesion/Cartes/Impression de cartes.html") as fp:
            soup = BeautifulSoup(fp, features="html.parser")
            divs = soup.find_all("div", {"class": "card recto"})

            for div in divs:
                if div.p:
                    paras = div.find_all("p")

                    if len(paras) == 5:
                        first_name = paras[0].text
                        last_name = paras[1].text
                        promo = paras[2].text.split(" ")[-1]
                        school_year = promo[0]
                        departement = promo[1:]
                        insa_student = True
                    else:
                        first_name = paras[0].text
                        last_name = paras[1].text
                        school_year = ""
                        departement = "Non Insalien"
                        insa_student = False

                    adhesion = Adhesion(
                        first_name=first_name,
                        last_name=last_name,
                        email=last_name.lower()
                        + "."
                        + first_name.lower()
                        + "@insa-rennes.fr",
                        insa_student=insa_student,
                        school_year=school_year,
                        departement=departement,
                    )

                    adhesion.save()

        return redirect("administration")
