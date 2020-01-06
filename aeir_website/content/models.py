from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from stdimage.validators import MinSizeValidator, MaxSizeValidator
from stdimage.models import StdImageField
from ckeditor.fields import RichTextField

# Create your models here.

POST = (
    ("Président", "Président"),
    ("Présidente", "Présidente"),
    ("Vice-Président", "Vice-Président"),
    ("Vice-Présidente", "Vice-Présidente"),
    ("Trésorier", "Trésorier"),
    ("Trésorière", "Trésorière"),
    ("Vice-Trésorier", "Vice-Trésorier"),
    ("Vice-Trésorière", "Vice-Trésorière"),
    ("Secrétaire", "Secrétaire"),
    ("Vice-Secrétaire", "Vice-Secrétaire"),
    ("Communication", "Communication"),
    ("Partenariats", "Partenariats"),
    ("Responsable Technique", "Responsable Technique"),
    ("Président du Foyer", "Président du Foyer"),
    ("Autre", "Autre"),
)


class GlobalWebsiteParameters(models.Model):
    frontpage_video = models.FileField(upload_to="global_parameters")
    default_adhesion_picture = StdImageField(
        upload_to="global_parameters",
        validators=[MinSizeValidator(230, 292), MaxSizeValidator(1080, 720)],
        variations={"thumbnail": {"width": 230, "height": 292, "crop": True}},
        default=None,
    )
    insa_description = RichTextField()
    aeir_description = RichTextField()
    adhesion_description = RichTextField()

    def __str__(self):
        return "Website parameters"


class News(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    date = models.DateField()
    picture = StdImageField(upload_to="news", validators=[MinSizeValidator(800, 600)],)

    def __str__(self):
        return self.title


class Club(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    logo = StdImageField(upload_to="club", validators=[MinSizeValidator(800, 600)],)
    mail = models.EmailField()
    website = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    logo = StdImageField(upload_to="partner", validators=[MinSizeValidator(800, 600)],)
    mail = models.EmailField()
    website = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    picture = StdImageField(upload_to="event", validators=[MinSizeValidator(800, 600)],)
    date = models.DateField()

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    picture = StdImageField(
        upload_to="team_member", validators=[MinSizeValidator(800, 600)],
    )
    post = models.CharField(max_length=200, choices=POST)
    mail = models.EmailField()

    def __str__(self):
        return self.first_name + " " + self.last_name
