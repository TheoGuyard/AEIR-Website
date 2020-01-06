import datetime
from django import forms
from .models import Adhesion
from captcha.fields import CaptchaField
from PIL import Image
from django.core.files import File
from .models import Adhesion

current_year = datetime.date.today().year
BIRTH_YEAR_CHOICES = [year for year in range(current_year - 100, current_year)]


class AdhesionForm(forms.ModelForm):

    captcha = CaptchaField()

    class Meta:
        model = Adhesion
        fields = [
            "first_name",
            "last_name",
            "birthday",
            "email",
            "picture",
            "school_year",
            "departement",
            "insa_student",
        ]
        widgets = {
            "birthday": forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
        }
        labels = {
            "first_name": "Nom de famille",
            "last_name": "Prénom",
            "birthday": "Date d'anniversaire",
            "email": "Adresse mail (INSA de préférence)",
            "picture": "Photo",
            "insa_student": "Je suis un étudiant INSA",
            "school_year": "Année d'étude",
            "departement": "Spécialité",
        }
