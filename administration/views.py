from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from adhesion.models import Adhesion
from adhesion.forms import AdhesionForm
from content.models import *
from content.forms import *
from .csv_extract import list_to_csv
from .forms import AdhesionFilter

### Connexion ###

class AdministrationLoginView(LoginView):
    template_name = 'administration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Login'
        context['page_subtitle'] = 'Identifez vous pour administrer le site'
        return context

class AdministrationLogoutView(LoginRequiredMixin, LogoutView):
    login_url = 'login'
    template_name = 'administration/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Logout'
        context['page_subtitle'] = 'À plus mon ptit !'
        return context

class AdministrationPermissionDeniedView(LoginRequiredMixin, TemplateView):
    login_url = 'administration_login'
    template_name = 'administration/permission_denied.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Accès refusé'
        return context

class AdministrationView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = ''
    template_name = 'administration/administration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Bienvenue '+str(self.request.user.first_name)+' '+str(self.request.user.last_name)+ ' !'
        return context

### Adhésions ###

class AdministrationAdherentListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    login_url = 'administration_login'
    template_name = 'administration/adherent_list.html'
    model = Adhesion
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Liste des adhérents'
        return context

    def get_queryset(self):
        return Adhesion.objects.filter(adhesion_type="Adhésion AEIR", paid=True).order_by('first_name')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

    def post(self, request):
        form = request.POST
        if 'card' in form:
            user = Adhesion.objects.get(id=int(form['card']))
            return user.card
        elif 'csv' in form:
            return list_to_csv(Adhesion.objects.filter(paid=True))
        else:
            redirect('')

class AdministrationAdherentUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    login_url = 'administration_login'
    template_name = 'administration/adherent_update.html'
    model = Adhesion
    form_class = AdhesionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = "Modification d'un adhérent"
        return context

    def get_success_url(self):
        return reverse('administration')

    def get_object(self, queryset=None):
        obj = Adhesion.objects.get(id=self.kwargs['id'])
        return obj
    
    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationAdherentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    login_url = 'administration_login'
    template_name = 'administration/adherent_delete.html'
    model = Adhesion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = "Suppression d'un adhérent"
        return context

    def get_object(self, queryset=None):
        obj = Adhesion.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return reverse('administration')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationNewAdherentListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    login_url = 'administration_login'
    template_name = 'administration/new_adherent_list.html'
    model = Adhesion
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Gestion des nouvelles adhérents'
        return context

    def get_queryset(self):
        return Adhesion.objects.filter(adhesion_type="Adhésion AEIR", paid=False).order_by('first_name')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationNewAdherentDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    login_url = 'administration_login'
    template_name = 'administration/new_adherent_detail.html'
    model = Adhesion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Détail d\'un nouvel adhérent'
        return context
    
    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

    def post(self, request, pk):
        form = request.POST
        print(form)
        

class AdministrationAdherentSearchView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    login_url = 'administration_login'
    template_name = 'administration/adherent_search.html'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Rechercher un amicaliste'
        context['filter'] = AdhesionFilter(self.request.GET, queryset=Adhesion.objects.filter(paid=True))
        return context

    def test_func(self):
        return self.request.user.groups.filter(name="Adhesion AEIR management").exists()

    def handle_no_permission(self):
        return redirect('administration_no_permission')

### Content ###

# News

class AdministrationNewsListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    login_url = 'administration_login'
    template_name = 'administration/news_list.html'
    model = News
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Page des actualités'
        return context

    def get_queryset(self):
        return News.objects.all().order_by('-date')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationNewsDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    login_url = 'administration_login'
    template_name = 'administration/news_detail.html'
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Détail d\'une actualité'
        return context
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationNewsCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    login_url = 'administration_login'
    template_name = 'administration/news_create.html'
    model = News
    form_class = NewsForm
    success_url = 'news_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Création d\'une actualité'
        return context
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationNewsUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    login_url = 'administration_login'
    template_name = 'administration/news_update.html'
    model = News
    form_class = NewsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Modification d\'une actualité'
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse('news_list')
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationNewsDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    login_url = 'administration_login'
    template_name = 'administration/news_delete.html'
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = "Suppression d'une news"
        return context

    def get_object(self, queryset=None):
        obj = News.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return reverse('news_list')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

# Team

class AdministrationTeamListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    login_url = 'administration_login'
    template_name = 'administration/team_list.html'
    model = TeamMember
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = "Membres de l'AEIR"
        return context

    def get_queryset(self):
        return TeamMember.objects.all()
    
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationTeamDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    login_url = 'administration_login'
    template_name = 'administration/team_detail.html'
    model = TeamMember

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Détail d\'un membre du bureau'
        return context
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationTeamCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    login_url = 'administration_login'
    template_name = 'administration/team_create.html'
    model = TeamMember
    form_class = TeamMemberForm
    success_url = 'team_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Création d\'un membre du bureau'
        return context
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationTeamUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    login_url = 'administration_login'
    template_name = 'administration/team_update.html'
    model = TeamMember
    form_class = TeamMemberForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Modification d\'un membre du bureau'
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse('team_list')
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationTeamDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    login_url = 'administration_login'
    template_name = 'administration/team_delete.html'
    model = TeamMember

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = "Suppression d'un membre du bureau"
        return context

    def get_object(self, queryset=None):
        obj = TeamMember.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return reverse('team_list')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

# Club

class AdministrationClubListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    login_url = 'administration_login'
    template_name = 'administration/club_list.html'
    model = Club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Page des clubs'
        return context

    def get_queryset(self):
        return Club.objects.all().order_by('name')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationClubDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    login_url = 'administration_login'
    template_name = 'administration/club_detail.html'
    model = Club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Détail d\'un club'
        return context
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationClubCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    login_url = 'administration_login'
    template_name = 'administration/club_create.html'
    model = Club
    form_class = ClubForm
    success_url = 'club_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Création d\'un club'
        return context
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationClubUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    login_url = 'administration_login'
    template_name = 'administration/club_update.html'
    model = Club
    form_class = ClubForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Modification d\'un club'
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse('club_list')
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationClubDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    login_url = 'administration_login'
    template_name = 'administration/club_delete.html'
    model = Club

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = "Suppression d'un club"
        return context

    def get_object(self, queryset=None):
        obj = Club.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return reverse('club_list')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

# Event

class AdministrationEventListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    login_url = 'administration_login'
    template_name = 'administration/event_list.html'
    model = Event
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Page des événements'
        return context

    def get_queryset(self):
        return Event.objects.all().order_by('date')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationEventDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    login_url = 'administration_login'
    template_name = 'administration/event_detail.html'
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Détail d\'un événement'
        return context
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationEventCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    login_url = 'administration_login'
    template_name = 'administration/event_create.html'
    model = Event
    form_class = EventForm
    success_url = 'event_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Création d\'un événement'
        return context
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationEventUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    login_url = 'administration_login'
    template_name = 'administration/event_update.html'
    model = Event
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Modification d\'un événement'
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse('event_list')
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationEventDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    login_url = 'administration_login'
    template_name = 'administration/event_delete.html'
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = "Suppression d'un événement"
        return context

    def get_object(self, queryset=None):
        obj = Event.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return reverse('event_list')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

# Partner

class AdministrationPartnerListView(UserPassesTestMixin, LoginRequiredMixin, ListView):

    login_url = 'administration_login'
    template_name = 'administration/partner_list.html'
    model = Partner
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Page des partenariats'
        return context

    def get_queryset(self):
        return Partner.objects.all().order_by('name')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationPartnerDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    login_url = 'administration_login'
    template_name = 'administration/partner_detail.html'
    model = Partner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Détail d\'un partenariat'
        return context
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationPartnerCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    login_url = 'administration_login'
    template_name = 'administration/partner_create.html'
    model = Partner
    form_class = PartnerForm
    success_url = 'partner_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Création d\'un partenariat'
        return context
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationPartnerUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    login_url = 'administration_login'
    template_name = 'administration/partner_update.html'
    model = Partner
    form_class = PartnerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = 'Modification d\'un partenariat'
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse('partner_list')
        
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')

class AdministrationPartnerDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    login_url = 'administration_login'
    template_name = 'administration/partner_delete.html'
    model = Partner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration'
        context['page_subtitle'] = "Suppression d'un partenrariat"
        return context

    def get_object(self, queryset=None):
        obj = Partner.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return reverse('partner_list')
    
    def test_func(self):
        return self.request.user.groups.filter(name="Content management").exists()

    def handle_no_permission(self):
        return redirect('permission_denied')