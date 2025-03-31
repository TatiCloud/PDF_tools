from PyPDF2 import PdfMerger


def merge_pdfs(pdf_list, output_filename):
    """
    Merges a list of PDF files into a single PDF file.

    :param pdf_list: List of PDF file paths to be merged.
    :param output_filename: The filename of the output merged PDF.
    """
    merger = PdfMerger()

    try:
        for pdf in pdf_list:
            merger.append(pdf)
        merger.write(output_filename)
        print(f"Merged PDFs saved as '{output_filename}'")
    except Exception as e:
        print(f"An error occurred while merging PDFs: {e}")
    finally:
        merger.close()


def get_user_input():
    """
    Gets user input for the PDF files to merge and the output filename.

    :return: Tuple containing list of PDF files and output filename.
    """
    pdf_files = []
    print("Enter the PDF file paths to merge (type 'done' when finished):")

    while True:
        file_path = input("Enter PDF file path: ").strip()
        if file_path.lower() == 'done':
            break
        elif file_path:
            pdf_files.append(file_path)
        else:
            print("Invalid input. Please enter a valid file path or 'done' to finish.")

    if not pdf_files:
        print("No PDF files were entered. Exiting...")
        return [], None

    output_file = input("Enter the output filename (e.g., 'merged.pdf'): ").strip()

    return pdf_files, output_file


def main():
    pdf_files, output_file = get_user_input()

    if pdf_files and output_file:
        merge_pdfs(pdf_files, output_file)
    else:
        print("Merging operation aborted.")


if __name__ == "__main__":
    main()
