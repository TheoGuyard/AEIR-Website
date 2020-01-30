import datetime
from django import forms
from django.core.files import File
from django.utils.safestring import mark_safe
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, HTML, Row, Column
from crispy_forms.bootstrap import InlineCheckboxes
from bootstrap_datepicker_plus import DatePickerInput
from .models import Adhesion

class AdhesionForm(forms.ModelForm):

    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("first_name"),
                Column("last_name"),
            ),
            Row(
                Column("birthday"),
                Column("email"),
            ),
            Row(
                Column(Field("picture")),
                Column("insa_student"),
            ),
            Row(
                Column("school_year"),
                Column("departement"),
            ),
            HTML("""<hr>"""),
            Row(
                Column(Field("captcha", css_class="form-control col-md-5 m-auto"), css_class="text-center"),
            ),
            HTML("""<hr>"""),
            HTML("""En validant votre adhésion, vous vous engagez également à respecter les <a href="{{ MEDIA_URL }}{{ cgv }}" target="_new">conditions
            générales d'adhésion à l'AEIR</a>."""),
            HTML("""<hr>"""),
            ButtonHolder(
                Submit("submit", "Valider", css_class="btn btn-primary hvr-grow"),
                css_class="text-center"
            ),
        )

    class Meta:
        model = Adhesion
        fields = ["first_name", "last_name", "birthday", "email", "picture", "insa_student", "school_year", "departement"]
        labels = {
            "first_name": "Nom de famille",
            "last_name": "Prénom",
            "birthday": "Date de naissance",
            "email": "Adresse mail (INSA de préférence)",
            "picture": "Photo",
            "insa_student": "Je suis un étudiant INSA",
            "school_year": "Année d'étude",
            "departement": "Spécialité",
        }
        widgets = {
            "birthday": DatePickerInput(format="%d/%m/%Y"),
            'picture': forms.FileInput(),
        }
