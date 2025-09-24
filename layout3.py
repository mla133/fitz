
import fitz  # PyMuPDF
import textwrap
import glob

PAGE_WIDTH, PAGE_HEIGHT = 612, 792  # US Letter
MARGIN = 60
LINE_HEIGHT = 16  # For fontsize=12

# Get a list of text files (e.g., all .txt files in a folder)
text_files = sorted(glob.glob("text/*.txt"))  # Adjust path as needed

doc = fitz.open()

for i, file_path in enumerate(text_files):
    with open(file_path, "r", encoding="utf-8") as f:
        file_text = f.read()
    # Wrap text for the page
    wrapper = textwrap.TextWrapper(width=90)
    lines = []
    for para in file_text.split('\n'):
        lines.extend(wrapper.wrap(para))
        lines.append('')  # Blank line between paragraphs

    lines_per_page = int((PAGE_HEIGHT - 2 * MARGIN) / LINE_HEIGHT)
    # If the file is too long, split into multiple pages
    chunks = [lines[j:j + lines_per_page] for j in range(0, len(lines), lines_per_page)]
    for chunk in chunks:
        page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        y = MARGIN
        for line in chunk:
            page.insert_text((MARGIN, y), line, fontname="helv", fontsize=12, color=(0.1, 0.1, 0.1))
            y += LINE_HEIGHT
        # Page number (bottom center)
        page_num_rect = fitz.Rect(PAGE_WIDTH / 2 - 20, PAGE_HEIGHT - 40, PAGE_WIDTH / 2 + 20, PAGE_HEIGHT - 20)
        page.insert_textbox(page_num_rect, str(doc.page_count), fontname="helv", fontsize=10, align=1, color=(0.2, 0.2, 0.2))

doc.save("multiple_files_per_page.pdf")
doc.close()
