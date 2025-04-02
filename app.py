import os
import PyPDF2
import logging
from tkinter import filedialog, Tk, simpledialog
from datetime import datetime

def browse_files(title, filetypes):
    """ Helper function to browse and select files """
    root = Tk()
    root.withdraw()  # Hide the root window
    return filedialog.askopenfilenames(title=title, filetypes=filetypes)

def split_pdf(pdf_file):
    if not pdf_file:
        logging.warning("No PDF file provided.")
        return

    logging.info(f"PDF selected: {pdf_file}")  # Debugging output

    # Ask the user to select a directory to save the split PDFs
    root = Tk()
    root.withdraw()  # Hide the root window
    output_dir = filedialog.askdirectory(title="Select Folder to Save Split PDFs")

    if not output_dir:  # If user cancels, exit
        logging.warning("No directory selected. Operation aborted.")
        return

    # Read the PDF
    try:
        with open(pdf_file, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            # Generate timestamp for naming files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            for i in range(num_pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(reader.pages[i])

                # Generate output filename for each split page
                output_pdf = os.path.join(output_dir, f"split_{timestamp}_page{i+1}.pdf")

                # Save the split page
                with open(output_pdf, "wb") as output_file:
                    writer.write(output_file)

                logging.info(f"Saved: {output_pdf}")
                print(f"Saved: {output_pdf}")  # Provide feedback to the user

    except Exception as e:
        logging.error(f"Error splitting PDF: {e}")


def merge_pdfs(pdf_list):
    writer = PyPDF2.PdfWriter()

    if not pdf_list:
        logging.warning("No PDF files provided.")
        return

    logging.info(f"PDFs selected: {pdf_list}")  # Debugging output

    # Ask the user to select a directory to save the merged PDF
    root = Tk()
    root.withdraw()  # Hide the root window
    output_dir = filedialog.askdirectory(title="Select Folder to Save Merged PDF")

    if not output_dir:  # If user cancels, exit
        logging.warning("No directory selected. Operation aborted.")
        return

    # Generate default filename with date and time (YYYYMMDD_HHMMSS format)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_pdf = os.path.join(output_dir, f"merged_{timestamp}.pdf")

    # Merge PDFs
    for pdf in sorted(pdf_list):
        try:
            with open(pdf, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    writer.add_page(page)
        except Exception as e:
            logging.error(f"Error opening {pdf}: {e}")

    # Save merged PDF
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    logging.info(f"Merged PDF saved at: {output_pdf}")
    print(f"Merged PDF saved at: {output_pdf}")  # Provide feedback to the user


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
    root = Tk()
    root.withdraw()  # Hide main window

    # Ask the user what they want to do
    action = simpledialog.askstring(
        "Select Action",
        "\nType 'split' to split a PDF,\n'merge' to merge PDFs,\n'or 'watermark' to add a watermark.",
    )

    if action.lower() not in ['split', 'merge', 'watermark']:
        print("Exiting...")
        return

    if action.lower() == 'split':
        # Choose the PDF to split
        pdf_file = browse_files("Select a PDF to split", [("PDF Files", "*.pdf")])
        if not pdf_file:
            print("No PDF selected. Exiting...")
            return

        # Split the PDF
        split_pdf(pdf_file[0])  # Call the split_pdf function to perform the action

    elif action.lower() == 'merge':
        # Choose multiple PDFs to merge
        pdf_files = browse_files("Select PDF files to merge", [("PDF Files", "*.pdf")])
        if not pdf_files:
            print("No PDFs selected. Exiting...")
            return

        merge_pdfs(pdf_files)

    elif action.lower() == 'watermark':
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

