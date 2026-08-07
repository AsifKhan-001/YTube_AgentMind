# from src.utils.file_manager import create_pdf_files
# from src.utils.save_markdown import save_markdown
import subprocess


def save_pdf(filename_markdown,filename_notesPDF):
    # filename_markdown = save_markdown()
    # filename_notesPDF = create_pdf_files()
    

    subprocess.run([
        "pandoc",
        filename_markdown,
        "--pdf-engine=xelatex",
        "-o",
        filename_notesPDF
    ],check=True)

    return filename_notesPDF