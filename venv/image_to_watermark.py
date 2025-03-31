from PIL import Image
import PyPDF2
from PyPDF2 import PdfWriter, PdfReader


def create_logo_watermark(input_image_path, transparency, output_image_path = "watermark_logo.png"):
    # Open the original image
    original = Image.open(input_image_path).convert("RGBA")

    # Apply transparency
    watermark = original.copy()
    watermark.putalpha(transparency)

    # Save the watermark image
    watermark.save(output_image_path, "PDF")


def add_logo_watermark(input_pdf, watermark_logo, output_logo_pdf):
    watermark_obj = PdfReader(watermark_logo)
    watermark_page = watermark_obj.pages[0]

    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[0]
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)

    with open(output_logo_pdf, 'wb') as out_file:
        pdf_writer.write(out_file)


if __name__ == "__main__":
    input_pdf = "../input_files/CAR PARK SPACE RENTAL AGREEMENT.pdf"  # Path to your input PDF file
    watermark_logo= "watermark_logo.png"
    output_logo_pdf = "output_logo_watermarked.pdf"
    input_image_path = "../input_files/input_image.png"
    #output_image_path = "watermark_logo.png"
    transparency = 128  # Transparency level (0-255), where 0 is completely transparent and 255 is completely opaque

    # Create a watermark PDF
    create_logo_watermark(input_image_path, transparency, output_image_path = "watermark_logo.png")

    # Add the watermark to each page of the input PDF
    add_logo_watermark(input_pdf, watermark_logo, output_logo_pdf)

    print(f"Watermark added to {output_logo_pdf}")
