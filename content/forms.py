from .models import *
from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget
from django.utils import timezone

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'date': SelectDateWidget(),
        }

class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = '__all__'

class TeamMemberForm(ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'

class PartnerForm(ModelForm):
    class Meta:
        model = Partner
        fields = '__all__'

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'date': SelectDateWidget(),
        }

