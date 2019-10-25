from django.db import models

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

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField()
    picture = models.ImageField(upload_to="news")

    def __str__(self):
        return self.title

class Club(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to="club")
    mail = models.EmailField()
    website = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to="partner")
    mail = models.EmailField()
    website = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    picture = models.ImageField(upload_to="event")
    date = models.DateField()

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="team_member")
    post = models.CharField(max_length=200, choices=POST)
    mail = models.EmailField()

    def __str__(self):
        return self.first_name + " " + self.last_name