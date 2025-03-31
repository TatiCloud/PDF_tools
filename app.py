import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog


def browse_files():
    root = tk.Tk()
    root.withdraw()  # Hide main window
    files_selected = filedialog.askopenfilenames(
        title="Select PDF Files",
        filetypes=[("PDF Files", "*.pdf")],  # Show only PDFs
    )
    return files_selected


def split_pdf(input_pdf, output_files):
    os.makedirs(output_files, exist_ok=True)
    with open(input_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for i in range(len(reader.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[i])
            output_filename = os.path.join(output_files, f"page_{i + 1}.pdf")
            with open(output_filename, "wb") as output_pdf:
                writer.write(output_pdf)


def merge_pdfs(pdf_files, output_pdf):
    writer = PyPDF2.PdfWriter()

    if not pdf_files:
        print("No PDF files provided.")
        return

    print(f"PDFs selected: {pdf_files}")  # Debugging output

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

    # Merge PDFs
    for pdf in sorted(pdf_files):
        try:
            with open(pdf, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    writer.add_page(page)
        except Exception as e:
            print(f"Error opening {pdf}: {e}")

    # Save merged PDF
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"Merged PDF saved as: {output_pdf}")


def add_watermark(input_pdf, watermark_pdf, output_pdf):
    with open(input_pdf, "rb") as file, open(watermark_pdf, "rb") as watermark_file:
        reader = PyPDF2.PdfReader(file)
        watermark_reader = PyPDF2.PdfReader(watermark_file)
        watermark_page = watermark_reader.pages[0]
        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)


if __name__ == "__main__":
    pdf_files = browse_files()  # Select PDFs manually
    if not pdf_files:
        print("No PDFs selected. Exiting...")
        exit()

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    merged_pdf = os.path.join(output_folder, "merged.pdf")

    merge_pdfs(pdf_files, merged_pdf)  # Pass list of files instead of a folder