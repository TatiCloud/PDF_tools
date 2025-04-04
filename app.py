import os
import logging
from datetime import datetime
from io import BytesIO
from tkinter import filedialog, Tk, simpledialog

import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def browse_files(title, filetypes):
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilenames(title=title, filetypes=filetypes)


def split_pdf(pdf_file):
    if not pdf_file:
        logging.warning("No PDF file provided.")
        return

    output_dir = filedialog.askdirectory(title="Select Folder to Save Split PDFs")
    if not output_dir:
        logging.warning("No directory selected. Operation aborted.")
        return

    try:
        with open(pdf_file, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            for i, page in enumerate(reader.pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(page)

                output_pdf = os.path.join(output_dir, f"split_{timestamp}_page{i+1}.pdf")
                with open(output_pdf, "wb") as output_file:
                    writer.write(output_file)

                print(f"Saved: {output_pdf}")
    except Exception as e:
        logging.error(f"Error splitting PDF: {e}")


def merge_pdfs(pdf_list):
    if not pdf_list:
        logging.warning("No PDF files provided.")
        return

    output_dir = filedialog.askdirectory(title="Select Folder to Save Merged PDF")
    if not output_dir:
        logging.warning("No directory selected. Operation aborted.")
        return

    output_pdf = os.path.join(output_dir, f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    writer = PyPDF2.PdfWriter()

    for pdf in sorted(pdf_list):
        try:
            with open(pdf, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    writer.add_page(page)
        except Exception as e:
            logging.error(f"Error opening {pdf}: {e}")

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"✅ Merged PDF saved at: {output_pdf}")


def create_watermark_pdf(watermark_text):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 40)
    can.setFillAlpha(0.2)
    can.drawCentredString(300, 500, watermark_text)
    can.save()
    packet.seek(0)
    return PyPDF2.PdfReader(packet)


def main():
    root = Tk()
    root.withdraw()

    action = simpledialog.askstring(
        "Select Action",
        "\nType 'split' to split a PDF,\n'merge' to merge PDFs,\n'or 'watermark' to add a watermark."
    )

    if action is None or action.lower() not in ['split', 'merge', 'watermark']:
        print("Exiting...")
        return

    if action.lower() == 'split':
        pdf_file = browse_files("Select a PDF to split", [("PDF Files", "*.pdf")])
        if not pdf_file:
            print("No PDF selected. Exiting...")
            return
        split_pdf(pdf_file[0])

    elif action.lower() == 'merge':
        pdf_files = browse_files("Select PDF files to merge", [("PDF Files", "*.pdf")])
        if not pdf_files:
            print("No PDFs selected. Exiting...")
            return
        merge_pdfs(pdf_files)

    elif action.lower() == 'watermark':
        pdf_files = browse_files("Select a PDF to watermark", [("PDF Files", "*.pdf")])
        if not pdf_files:
            print("No PDF selected. Exiting...")
            return
        input_pdf_path = pdf_files[0]

        watermark_text = simpledialog.askstring("Watermark Text", "Enter the watermark text:")
        if not watermark_text:
            print("No watermark text provided. Exiting...")
            return

        output_folder = filedialog.askdirectory(title="Select Folder to Save Watermarked PDF")
        if not output_folder:
            print("No folder selected. Exiting...")
            return

        output_pdf_path = os.path.join(output_folder, f"watermarked_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

        try:
            with open(input_pdf_path, "rb") as input_file:
                reader = PyPDF2.PdfReader(input_file)
                watermark_reader = create_watermark_pdf(watermark_text)
                watermark_page = watermark_reader.pages[0]

                writer = PyPDF2.PdfWriter()
                for page in reader.pages:
                    page.merge_page(watermark_page)
                    writer.add_page(page)

                with open(output_pdf_path, "wb") as output_file:
                    writer.write(output_file)

            print(f"✅ Watermarked PDF saved at: {output_pdf_path}")

        except Exception as e:
            print(f"❌ Error adding watermark: {e}")


if __name__ == "__main__":
    main()
