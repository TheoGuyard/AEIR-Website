from django.http import HttpResponse
from django.templatetags.static import static
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from content.models import GlobalWebsiteParameters


def generate_card(adhesion):

    # Create the response file
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="' + str(adhesion)

    # Create the background
    c = canvas.Canvas(response)
    c.drawImage(static("card/AEIR_card_model.png"), 0, 0, width=595.27, height=841.89)

    # Write informations
    if len(adhesion.last_name) > 10:
        c.setFont("Helvetica-Bold", 25)
    else:
        c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(150, 620, adhesion.last_name)

    if len(adhesion.first_name) > 10:
        c.setFont("Helvetica-Bold", 25)
    else:
        c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(150, 575, adhesion.first_name)

    c.line(40, 555, 260, 555)

    c.setFont("Helvetica", 17)

    c.drawCentredString(150, 520, adhesion.email)

    birthday_day = str(adhesion.birthday).split("-")[2]
    birthday_month = str(adhesion.birthday).split("-")[1]
    birthday_year = str(adhesion.birthday).split("-")[0]
    c.drawCentredString(
        150, 500, "Né le " + birthday_day + "/" + birthday_month + "/" + birthday_year
    )

    if adhesion.insa_student:
        c.drawCentredString(150, 480, "Insalien")
    else:
        c.drawCentredString(150, 480, "Non Insalien")

    if adhesion.school_year != "Autre" and adhesion.departement != "Autre":
        c.drawCentredString(150, 460, adhesion.school_year + " " + adhesion.departement)
    else:
        c.drawCentredString(150, 460, "Promotion non renseignée")

    c.line(40, 440, 260, 440)

    c.setFont("Helvetica-Bold", 17)

    c.drawCentredString(150, 410, "Année : " + str(adhesion.year))

    if adhesion.paid and adhesion.valid_infos:
        c.setFillColorRGB(0, 128, 0)
        c.drawCentredString(150, 390, "Adhesion validée")
    else:
        c.setFillColorRGB(255, 0, 0)
        c.drawCentredString(150, 390, "Adhesion non validée")

    # Display picture
    if adhesion.picture:
        c.drawImage(adhesion.picture.thumbnail.path, 314, 365, height=292, width=230)
    else:
        c.drawImage(
            GlobalWebsiteParameters.objects.all()
            .first()
            .default_adhesion_picture.thumbnail.path,
            314,
            365,
            height=292,
            width=230,
        )

    # Barcode and adherent number
    c.setFillColorRGB(0, 0, 0)
    barcode = code128.Code128(str(adhesion.id), barWidth=3.6, barHeight=60)
    barcode.drawOn(c, 180, 260)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(328, 240, "Numéro d'adhérent : " + str(adhesion.get_number))

    c.showPage()
    c.save()
    return response
