import csv
from django.http import HttpResponse
from adhesion.models import Adhesion, ArchivedAdhesion


def list_to_csv(objects):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="liste.csv"'
    writer = csv.writer(response)
    writer.writerow([f.name for f in Adhesion._meta.fields])
    for obj in objects:
        writer.writerow([field.value_to_string(obj) for field in obj._meta.fields])
    return response


def list_to_csv_event(objects):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="liste.csv"'
    writer = csv.writer(response)
    writer.writerow(["Nom", "Prénom", "Promo"])
    for obj in objects:
        writer.writerow([obj.first_name, obj.last_name, obj.promo])
    return response


def old_list_to_csv(objects):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="liste.csv"'
    writer = csv.writer(response)
    writer.writerow([f.name for f in ArchivedAdhesion._meta.fields])
    for obj in objects:
        writer.writerow([field.value_to_string(obj) for field in obj._meta.fields])
    return response
