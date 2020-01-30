import random
import string
import datetime
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from .card import generate_card
from stdimage.validators import MinSizeValidator, MaxSizeValidator
from stdimage.models import StdImageField


# Create your models here.


def random_id():
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(8)]
    )


SCHOOL_YEAR = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("Autre", "Autre"),
)

DEPARTEMENT = (
    ("STPI", "STPI"),
    ("GM", "GM"),
    ("INFO", "INFO"),
    ("SRC", "SRC"),
    ("EII", "EII"),
    ("GMA", "GMA"),
    ("SGM", "SGM"),
    ("GCU", "GCU"),
    ("CDTI", "CDTI"),
    ("Autre", "Autre"),
)

BINARY_CHOICE = (
    (True, "Oui"),
    (False, "Non"),
)


class Adhesion(models.Model):

    # Personal infos
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birthday = models.DateField(default=datetime.date.today)
    email = models.EmailField()
    picture = StdImageField(
        upload_to="adhesion_aeir",
        validators=[MinSizeValidator(230, 292), MaxSizeValidator(1080, 720)],
        variations={"thumbnail": {"width": 230, "height": 292, "crop": True}},
    )

    # Schooling infos
    insa_student = models.BooleanField(default=False, choices=BINARY_CHOICE)
    school_year = models.CharField(max_length=200, choices=SCHOOL_YEAR)
    departement = models.CharField(max_length=200, choices=DEPARTEMENT)

    # Administration infos
    adhesion_date = models.DateField(auto_now_add=True)
    card_id = models.CharField(max_length=8, default=random_id)
    card_pwd = models.CharField(max_length=8, default=random_id)
    paid = models.BooleanField(default=False)
    valid_infos = models.BooleanField(default=True)

    # School year of an adhesion (which goes from august 1st to july 31st)
    @property
    def year(self):
        if self.adhesion_date.month <= 7:
            return (
                str(self.adhesion_date.year - 1) + " - " + str(self.adhesion_date.year)
            )
        else:
            return (
                str(self.adhesion_date.year) + " - " + str(self.adhesion_date.year + 1)
            )

    @property
    def card(self):
        return generate_card(self)

    @property
    def get_number(self):
        if self.adhesion_date.month <= 7:
            return (
                int(
                    str(self.adhesion_date.year - 1)[2:]
                    + str(self.adhesion_date.year)[2:]
                )
                * 10 ** 5
                + self.id
            )
        else:
            return (
                int(
                    str(self.adhesion_date.year)[2:]
                    + str(self.adhesion_date.year + 1)[2:]
                )
                * 10 ** 5
                + self.id
            )

    @property
    def promo(self):
        if self.departement != "Autre" and self.school_year != "Autre":
            return self.school_year + " " + self.departement
        elif self.departement != "Autre":
            return self.departement
        elif self.school_year != "Autre":
            return self.school_year + " " + "A"
        else:
            return "Non précisé"

    def __str__(self):
        return self.first_name + " " + self.last_name


class ArchivedAdhesion(models.Model):

    # Personal infos
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()

    # Schooling infos
    insa_student = models.BooleanField()
    school_year = models.CharField(max_length=200)
    departement = models.CharField(max_length=200)

    # Administration infos
    adhesion_date = models.DateField()
    year = models.IntegerField()

    @property
    def promo(self):
        if self.departement != "Autre" and self.school_year != "Autre":
            return self.school_year + " " + self.departement
        elif self.departement != "Autre":
            return self.departement
        elif self.school_year != "Autre":
            return self.school_year + " " + "A"
        else:
            return "Non précisé"

    def send_mail(self):

        ### IMPORTANT ###
        email = 'guyard.theo@gmail.com'
        # email = self.mail
        send_mail("Réadhésion à l\'AEIR", "Bonjour, \n Vous pouvez désormais vous résincrire à l'AIER à l'adresse suivante : aeir.insa-rennes.fr ! \n Bonne journée !", 
            settings.EMAIL_HOST_USER,
            [email], fail_silently=False)

    def attrs(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    def __str__(self):
        return self.first_name + " " + self.last_name
