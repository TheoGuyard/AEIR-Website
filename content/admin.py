from django.contrib import admin
from .models import News, Club, Partner, Event, TeamMember

# Register your models here.

admin.site.register(News)
admin.site.register(Club)
admin.site.register(Partner)
admin.site.register(Event)
admin.site.register(TeamMember)