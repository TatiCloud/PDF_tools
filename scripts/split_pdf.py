import PyPDF2
import os

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