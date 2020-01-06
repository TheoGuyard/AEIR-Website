from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128


def generate_card(adhesion):

    # Create the response file
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="' + str(adhesion)

    # Create the background
    c = canvas.Canvas(response)
    c.drawImage("static/card/AEIR_card_model.png", 0, 0, width=595.27, height=841.89)

    # Write informations
    if len(adhesion.last_name) > 10:
        c.setFont("Helvetica-Bold", 25)
    else:
        c.setFont("Helvetica-Bold", 40)

    c.drawCentredString(150, 600, adhesion.last_name)

    if len(adhesion.first_name) > 10:
        c.setFont("Helvetica-Bold", 25)
    else:
        c.setFont("Helvetica-Bold", 40)

    c.drawCentredString(150, 550, adhesion.first_name)

    if adhesion.insa_student:
        c.drawCentredString(150, 430, "Insalien")
    else:
        c.drawCentredString(150, 430, "Non Insalien")

    if adhesion.school_year != "Autre" and adhesion.departement != "Autre":
        c.drawCentredString(150, 430, adhesion.school_year + " " + adhesion.departement)
    else:
        c.drawCentredString(150, 430, "Promotion non renseignée")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(150, 460, "Année d'adhésion : " + str(adhesion.year))

    if adhesion.paid:
        c.setFillColorRGB(0, 128, 0)
        c.drawCentredString(150, 400, "Adhesion payée")
    else:
        c.setFillColorRGB(255, 0, 0)
        c.drawCentredString(150, 400, "Adhesion non payée")

    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(150, 370, "Né le " + str(adhesion.birthday))

    # Display picture
    c.drawImage(adhesion.picture.thumbnail.path, 314, 365, height=292, width=230)

    # Barcode and adherent number
    c.setFillColorRGB(0, 0, 0)
    barcode = code128.Code128(str(adhesion.id), barWidth=5, barHeight=60)
    barcode.drawOn(c, 180, 260)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(312, 240, "Numéro d'adhérent : " + str(adhesion.id))

    c.showPage()
    c.save()
    return response
