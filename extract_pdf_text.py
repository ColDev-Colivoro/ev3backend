import pypdf
import os


def extract_text_from_pdf(pdf_path, output_file):
    output_file.write(f"--- Extracting text from: {pdf_path} ---\n")
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        output_file.write(text)
    except Exception as e:
        output_file.write(f"Error reading {pdf_path}: {e}\n")
    output_file.write(f"--- End of {pdf_path} ---\n\n")


pdf_files = ["TI3041 - Ev.3.pdf", "TI3041 - Ev.3 (1).pdf"]

with open("pdf_content.txt", "w", encoding="utf-8") as f:
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            extract_text_from_pdf(pdf_file, f)
        else:
            f.write(f"File not found: {pdf_file}\n")
