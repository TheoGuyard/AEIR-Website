from .models import *
from django.forms import ModelForm, CharField, FileInput, ClearableFileInput
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import InlineCheckboxes
from bootstrap_datepicker_plus import DatePickerInput


class GlobalWebsiteParametersForm(ModelForm):
    insa_description = CharField(widget=CKEditorWidget(), label="Description de l'INSA")
    aeir_description = CharField(widget=CKEditorWidget(), label="Description de l'AEIR")
    adhesion_description = CharField(
        widget=CKEditorWidget(), label="Texte de la page d'adhésion"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("frontpage_video"),
            HTML("""<hr>"""),
            Field("default_adhesion_picture"),
            HTML("""<hr>"""),
            Field("conditions_adhesion"),
            HTML("""<hr>"""),
            Field("insa_description"),
            Field("aeir_description"),
            Field("adhesion_description"),
            HTML("""<hr>"""),
            ButtonHolder(
                Submit("submit", "Valider", css_class="btn-primary hvr-grow"),
                css_class="text-center",
            ),
        )

    class Meta:
        model = GlobalWebsiteParameters
        fields = "__all__"
        labels = {
            "frontpage_video": "Video de la page d'accueil",
            "default_adhesion_picture": "Photo d'adhésion par défaut",
            "conditions_adhesion": "Conditions générales de l'AEIR",
            "insa_description": "Description de l'INSA",
            "aeir_description": "Description de l'AEIR",
            "adhesion_description": "Texte de la page d'adhésion",
        }
        widgets = {
            'frontpage_video': ClearableFileInput(),
            'default_adhesion_picture': ClearableFileInput(),
            'conditions_adhesion': ClearableFileInput(),
        }
        


class NewsForm(ModelForm):
    content = CharField(widget=CKEditorWidget(), label="Contenu")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("title"),
            Field("content"),
            Field("date"),
            Field("picture"),
            HTML("""<hr>"""),
            ButtonHolder(
                Submit("submit", "Valider", css_class="btn-primary hvr-grow"),
                css_class="text-center",
            ),
        )

    class Meta:
        model = News
        fields = "__all__"
        labels = {
            "title": "Titre",
            "content": "Contenu",
            "date": "Date",
            "picture": "Illustration",
        }
        widgets = {
            "date": DatePickerInput(format="%d/%m/%Y"),
            'picture': ClearableFileInput(),
        }


class ClubForm(ModelForm):
    description = CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name"),
            Field("description"),
            Field("logo"),
            Field("mail"),
            Field("website"),
            HTML("""<hr>"""),
            ButtonHolder(
                Submit("submit", "Valider", css_class="btn-primary hvr-grow"),
                css_class="text-center",
            ),
        )

    class Meta:
        model = Club
        fields = "__all__"
        labels = {
            "name": "Nom du club",
            "description": "Description",
            "logo": "Logo",
            "mail": "Email",
            "website": "Site internet",
        }
        widgets = {
            'logo': ClearableFileInput(),
        }


class TeamMemberForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("first_name"),
            Field("last_name"),
            Field("picture"),
            Field("post"),
            Field("mail"),
            HTML("""<hr>"""),
            ButtonHolder(
                Submit("submit", "Valider", css_class="btn-primary hvr-grow"),
                css_class="text-center",
            ),
        )

    class Meta:
        model = TeamMember
        fields = "__all__"
        labels = {
            "first_name": "Nom",
            "last_name": "Prénom",
            "picture": "Photo",
            "post": "Poste",
            "mail": "Email",
        }
        widgets = {
            'picture': ClearableFileInput(),
        }


class PartnerForm(ModelForm):
    description = CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name"),
            Field("description"),
            Field("logo"),
            Field("mail"),
            Field("website"),
            HTML("""<hr>"""),
            ButtonHolder(
                Submit("submit", "Valider", css_class="btn-primary hvr-grow"),
                css_class="text-center",
            ),
        )

    class Meta:
        model = Partner
        fields = "__all__"
        labels = {
            "name": "Nom du partenariat",
            "description": "Description",
            "logo": "Logo",
            "mail": "Email",
            "website": "Site internet",
        }
        widgets = {
            'logo': ClearableFileInput(),
        }


class EventForm(ModelForm):
    description = CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name"),
            Field("date"),
            Field("description"),
            Field("picture"),
            HTML("""<hr>"""),
            ButtonHolder(
                Submit("submit", "Valider", css_class="btn-primary hvr-grow"),
                css_class="text-center",
            ),
        )

    class Meta:
        model = Event
        fields = "__all__"
        labels = {
            "name": "Nom de l'événement",
            "description": "Description",
            "date": "Date",
            "picture": "Illustration",
        }
        widgets = {
            "date": DatePickerInput(format="%d/%m/%Y"),
            'picture': ClearableFileInput(),
        }

