from flask import Flask, request, send_file, render_template_string
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

app = Flask(__name__)

def create_certificate(student_name):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Border
    c.setStrokeColor(colors.green)
    c.setLineWidth(6)
    c.rect(40, 40, width - 80, height - 80)

    # Title
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(colors.darkgreen)
    c.drawCentredString(width / 2, height - 120, "Certificate of Achievement")

    # Subtitle
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 160, "This certificate is proudly presented to")

    # Student Name
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - 220, student_name)

    # Body Text
    text = (
        "For successfully completing the GreenLearn program on Ecology & Sustainability.\n"
        "Your dedication to learning about the environment and sustainable living\n"
        "will help shape a greener future for our planet. 🌱"
    )
    c.setFont("Helvetica", 14)
    for i, line in enumerate(text.split("\n")):
        c.drawCentredString(width / 2, height - 280 - (i * 20), line)

    # Signature
    c.line(width/2 - 150, 120, width/2 + 150, 120)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, 100, "Ecofinity Program Coordinator")

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width/2, 60, "Ecofinity • GreenLearn Initiative")

    c.save()
    buffer.seek(0)
    return buffer

@app.route("/certificate")
def certificate():
    name = request.args.get("name", "Student")
    pdf_buffer = create_certificate(name)
    return send_file(pdf_buffer, as_attachment=True,
                     download_name="certificate.pdf",
                     mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
