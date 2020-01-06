from django.http import HttpResponse
import csv


def list_to_csv(objects):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="liste.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "Type d'adhésion",
            "Nom",
            "Prénom",
            "Date d'anniversaire",
            "Mail",
            "Etudiant INSA",
            "Année d'étude",
            "Déparetement",
            "Date d'adhésion",
            "Année d'adhésion",
        ]
    )
    for obj in objects:
        writer.writerow(
            [
                obj.adhesion_type,
                obj.first_name,
                obj.last_name,
                obj.birthday,
                obj.email,
                obj.insa_student,
                obj.school_year,
                obj.departement,
                obj.adhesion_date,
                obj.year,
            ]
        )
    return response


def old_list_to_csv(objects):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="liste.csv"'
    writer = csv.writer(response)
    writer.writerow(
        ["Type d'adhésion", "Nom", "Prénom", "Promo", "Email", "Année d'adhésion"]
    )
    for obj in objects:
        writer.writerow(
            [
                obj.adhesion_type,
                obj.first_name,
                obj.last_name,
                obj.promo,
                obj.email,
                obj.year,
            ]
        )
    return response
