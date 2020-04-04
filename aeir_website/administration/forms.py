from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget
from aeir_website.adhesion.models import Adhesion, ArchivedAdhesion
from .models import EventManagement
from django_filters import FilterSet, NumberFilter, CharFilter
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import InlineCheckboxes
from bootstrap_datepicker_plus import DatePickerInput


class AdhesionFilter(FilterSet):
    first_name = CharFilter(
        field_name="first_name", lookup_expr="contains", label="Nom"
    )
    last_name = CharFilter(
        field_name="last_name", lookup_expr="contains", label="Prénom"
    )
    school_year = NumberFilter(
        field_name="school_year", lookup_expr="exact", label="Année"
    )
    departement = NumberFilter(
        field_name="departement", lookup_expr="exact", label="Département"
    )
    id = NumberFilter(field_name="id", lookup_expr="exact", label="Numéro d'adhérent")

    class Meta:
        model = Adhesion
        fields = []


class EventManagementForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name"),
            Field("date"),
            Field("max_capacity"),
            HTML("""<hr>"""),
            ButtonHolder(
                Submit("submit", "Valider", css_class="btn-primary hvr-grow"),
                css_class="text-center",
            ),
        )

    class Meta:
        model = EventManagement
        fields = ["name", "date", "max_capacity"]
        widgets = {
            "date": DatePickerInput(format="%d/%m/%Y"),
        }
        labels = {
            "name": "Nom de l'événement",
            "date": "Date",
            "max_capacity": "Capacité maximale",
        }


class ArchivedAdhesionFilter(FilterSet):
    first_name = CharFilter(
        field_name="first_name", lookup_expr="contains", label="Nom"
    )
    last_name = CharFilter(
        field_name="last_name", lookup_expr="contains", label="Prénom"
    )
    year = NumberFilter(
        field_name="year", lookup_expr="exact", label="Année"
    )

    class Meta:
        model = ArchivedAdhesion
        fields = []
