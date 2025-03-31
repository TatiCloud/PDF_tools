import PyPDF2
import os


def split_pdf(input_pdf, output_files):
    os.makedirs(output_folder, exist_ok=True)
    with open(input_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for i in range(len(reader.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[i])
            output_filename = os.path.join(output_files, f"page_{i + 1}.pdf")
            with open(output_filename, "wb") as output_pdf:
                writer.write(output_pdf)


def merge_pdfs(input_folder, output_pdf):
    writer = PyPDF2.PdfWriter()

    # Get all PDFs from the folder
    pdf_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".pdf")]

    # Sort files to maintain order
    for pdf in sorted(pdf_files):
        with open(pdf, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                writer.add_page(page)

    # Write merged PDF to output file
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)


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
    input_folder = "input_folder"
    output_folder = "output"
    split_folder = os.path.join(output_folder, "split")
    merged_pdf = os.path.join(output_folder, "merged.pdf")
    watermarked_pdf = os.path.join(output_folder, "watermarked.pdf")

    # Example Usage
    # split_pdf(os.path.join(input_folder, "sample.pdf"), split_folder)
    merge_pdfs("input_folder", "output_pdfs/Birth_Certificate_Amairah.pdf")
    # add_watermark(os.path.join(input_folder, "sample.pdf"), os.path.join(input_folder, "watermark.pdf"),
                  # watermarked_pdf)