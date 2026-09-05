from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(product_name, price, quantity, total):
    pdf = SimpleDocTemplate("invoice.pdf")
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>GROCERY STORE MANAGEMENT</b>", styles["Title"]))
    content.append(Paragraph("<br/>", styles["Normal"]))

    content.append(Paragraph(f"<b>Product:</b> {product_name}", styles["Normal"]))
    content.append(Paragraph(f"<b>Price:</b> ₹{price}", styles["Normal"]))
    content.append(Paragraph(f"<b>Quantity:</b> {quantity}", styles["Normal"]))
    content.append(Paragraph(f"<b>Total:</b> ₹{total}", styles["Normal"]))

    content.append(Paragraph("<br/>", styles["Normal"]))
    content.append(Paragraph("<b>Thank You! Visit Again.</b>", styles["Heading2"]))

    pdf.build(content)

    print("\n✅ PDF Invoice Generated Successfully!")
    print("📄 File Name: invoice.pdf")