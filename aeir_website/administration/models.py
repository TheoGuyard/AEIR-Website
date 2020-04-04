from django.db import models
from aeir_website.adhesion.models import Adhesion

# Create your models here.


class EventManagement(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    participants = models.ManyToManyField(Adhesion, default=0, blank=True)
    participants_non_adherents = models.IntegerField(default=0)
    max_capacity = models.IntegerField(default=800, blank=True)

    @property
    def total_participants(self):
        return len(self.participants.all()) + self.participants_non_adherents

    @property
    def surcapacity(self):
        return self.total_participants > self.max_capacity

    def __str__(self):
        return self.name
