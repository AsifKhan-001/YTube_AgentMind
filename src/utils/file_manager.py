import os



def create_markdown_files():
    counter = 1

    # 🛠️ Check for the file INSIDE the Markdown_files directory
    while os.path.exists(f"outputs/markdown/lecture_notes{counter}.md"):
        counter += 1

    # 📝 Create the unique filename
    filename = f"outputs/markdown/lecture_notes{counter}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Lecture Notes\n\n")


    print(f"✅ Created: {filename}")

    return filename


def create_pdf_files():

    # folder = "output/pdf"
    counter = 1

    # 🛠️ Keep checking until we find a number that doesn't exist yet
    while os.path.exists(f"outputs/pdf/lecture_notes{counter}.pdf"):
        counter += 1

    # 📝 Create the final unique filename
    filename_notesPDF = f"outputs/pdf/lecture_notes{counter}.pdf"

    print(f"✅ Will create: {filename_notesPDF}")

    return filename_notesPDF