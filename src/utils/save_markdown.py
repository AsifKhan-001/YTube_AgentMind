from src.utils.file_manager import create_markdown_files

# filename = create_markdown_files()

def save_markdown(markdow_notes,filename):
    with open(filename, "a", encoding="utf-8") as f:
        f.write("\n---\n\n")
        f.write(markdow_notes.strip())
        f.write("\n\n")

    return filename