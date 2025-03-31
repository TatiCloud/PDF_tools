# Software that add a watermark on PDF documents

import PyPDF2
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def create_watermark(watermark_text, output='watermark.pdf'):
    c = canvas.Canvas(output, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 45)
    c.setFillColorRGB(0.6, 0.6, 0.6, alpha=0.3)  # Light grey color with transparency
    c.saveState()
    c.translate(width / 2, height / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, watermark_text)
    c.restoreState()
    c.save()


def add_watermark(input_pdf, watermark_pdf, output_pdf):
    watermark_obj = PdfReader(watermark_pdf)
    watermark_page = watermark_obj.pages[0]

    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[0]
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)

    with open(output_pdf, 'wb') as out_file:
        pdf_writer.write(out_file)


if __name__ == "__main__":
    watermark_text = "Tati's Cloud Hub"
    input_pdf = "./input_folder/CAR PARK SPACE RENTAL AGREEMENT.pdf"  # Path to your input_folder PDF file
    watermark_pdf = "watermark.pdf"
    output_pdf = "output_watermarked.pdf"

    # Create a watermark PDF
    create_watermark(watermark_text, watermark_pdf)

    # Add the watermark to each page of the input_folder PDF
    add_watermark(input_pdf, watermark_pdf, output_pdf)

    print(f"Watermark added to {output_pdf}")
