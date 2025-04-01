import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog


def browse_files(title, filetypes):
    root = tk.Tk()
    root.withdraw()  # Hide main window
    files_selected = filedialog.askopenfilenames(
        title=title,
        filetypes=filetypes,
    )
    return files_selected


def split_pdf(input_pdf, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    with open(input_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for i in range(len(reader.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[i])
            output_filename = os.path.join(output_folder, f"page_{i + 1}.pdf")
            with open(output_filename, "wb") as output_pdf:
                writer.write(output_pdf)
    print(f"PDF split into individual pages in folder: {output_folder}")


def merge_pdfs(pdf_list, output_pdf):
    writer = PyPDF2.PdfWriter()

    if not pdf_list:
        print("No PDF files provided.")
        return

    print(f"PDFs selected: {pdf_list}")  # Debugging output

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

    # Merge PDFs
    for pdf in sorted(pdf_list):
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
    print(f"Watermarked PDF saved as: {output_pdf}")


def main():
    root = tk.Tk()
    root.withdraw()  # Hide main window

    # Ask the user what they want to do
    action = simpledialog.askstring(
        "Select Action",
        "What would you like to do?\nType 'split' to split a PDF,\n'to merge' to merge PDFs,\n'or 'watermark' to add a watermark.",
    )

    if action not in ['split', 'merge', 'watermark']:
        print("Invalid option selected. Exiting...")
        return

    if action == 'split':
        # Choose the PDF to split
        pdf_files = browse_files("Select a PDF to split", [("PDF Files", "*.pdf")])
        if not pdf_files:
            print("No PDF selected. Exiting...")
            return

        output_folder = simpledialog.askstring(
            "Output Folder", "Enter the output folder for the split files:"
        )
        split_pdf(pdf_files[0], output_folder)

    elif action == 'merge':
        # Choose multiple PDFs to merge
        pdf_files = browse_files("Select PDF files to merge", [("PDF Files", "*.pdf")])
        if not pdf_files:
            print("No PDFs selected. Exiting...")
            return

        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        merged_pdf = os.path.join(output_folder, "merged.pdf")
        merge_pdfs(pdf_files, merged_pdf)

    elif action == 'watermark':
        # Choose the input PDF and the watermark PDF
        pdf_files = browse_files("Select a PDF to watermark", [("PDF Files", "*.pdf")])
        if not pdf_files:
            print("No PDF selected. Exiting...")
            return

        watermark_files = browse_files("Select a watermark PDF", [("PDF Files", "*.pdf")])
        if not watermark_files:
            print("No watermark PDF selected. Exiting...")
            return

        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        watermarked_pdf = os.path.join(output_folder, "watermarked.pdf")
        add_watermark(pdf_files[0], watermark_files[0], watermarked_pdf)


if __name__ == "__main__":
    main()
