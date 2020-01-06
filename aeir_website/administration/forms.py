from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget
from adhesion.models import Adhesion, ArchivedAdhesion
from .models import EventManagement
from django_filters import FilterSet
import datetime


class AdhesionFilter(FilterSet):
    class Meta:
        model = Adhesion
        fields = {
            "first_name": ["contains"],
            "last_name": ["contains"],
            "school_year": ["exact"],
            "departement": ["exact"],
            "id": ["exact"],
        }


class EventManagementForm(ModelForm):
    class Meta:
        model = EventManagement
        fields = ["name", "date", "max_capacity"]
        widgets = {
            "date": SelectDateWidget(),
        }


class ArchivedAdhesionFilter(FilterSet):
    class Meta:
        model = ArchivedAdhesion
        fields = {
            "year": ["exact"],
        }
        labels = {
            "year": "Année",
        }
