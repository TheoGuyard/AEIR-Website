from .models import *
from django.forms import ModelForm, CharField
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from ckeditor.widgets import CKEditorWidget


class GlobalWebsiteParametersForm(ModelForm):
    insa_description = CharField(widget=CKEditorWidget())
    aeir_description = CharField(widget=CKEditorWidget())
    adhesion_description = CharField(widget=CKEditorWidget())

    class Meta:
        model = GlobalWebsiteParameters
        fields = "__all__"


class NewsForm(ModelForm):
    content = CharField(widget=CKEditorWidget())

    class Meta:
        model = News
        fields = "__all__"
        widgets = {
            "date": SelectDateWidget(),
        }


class ClubForm(ModelForm):
    description = CharField(widget=CKEditorWidget())

    class Meta:
        model = Club
        fields = "__all__"


class TeamMemberForm(ModelForm):
    class Meta:
        model = TeamMember
        fields = "__all__"


class PartnerForm(ModelForm):
    description = CharField(widget=CKEditorWidget())

    class Meta:
        model = Partner
        fields = "__all__"


class EventForm(ModelForm):
    description = CharField(widget=CKEditorWidget())

    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "date": SelectDateWidget(),
        }
