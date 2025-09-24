import fitz  # PyMuPDF
import textwrap

# Constants for US Letter size and layout
PAGE_WIDTH, PAGE_HEIGHT = 612, 792  # US Letter in points
MARGIN = 60
TEXT_FONT_SIZE = 30
LINE_HEIGHT = int(1.5 * TEXT_FONT_SIZE)

# Sample content
title = "The Art of Python"
author = "Matthew Allen"
body_text = (
    "Python is a versatile programming language loved by developers worldwide. "
    "Its clear syntax and powerful libraries make it ideal for everything from web development "
    "to data science and artificial intelligence. This eBook explores Python's strengths, "
    "best practices, and practical examples to help you master the language.\n\n"
) * 45  # Repeat to simulate long content

# Create a new PDF document
doc = fitz.open()

# --- Cover Page ---
cover = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)

# Title
title_rect = fitz.Rect(MARGIN, 120, PAGE_WIDTH - MARGIN, 180)
cover.insert_textbox(title_rect, title, fontname="helv", fontsize=28, align=1, color=(0, 0, 0.5))
cover.draw_rect(title_rect, color=(1, 0, 0), width=1)  # Red border

# Author
author_rect = fitz.Rect(MARGIN, 190, PAGE_WIDTH - MARGIN, 220)
cover.insert_textbox(author_rect, f"by {author}", fontname="helv", fontsize=16, align=1, color=(0.3, 0.3, 0.3))
cover.draw_rect(author_rect, color=(0, 1, 0), width=1)  # Green border

# Horizontal line separator
line_y = 235
cover.draw_line((MARGIN, line_y), (PAGE_WIDTH - MARGIN, line_y), color=(0.7, 0.7, 0.7), width=1)

# --- Prepare body text ---
usable_width = PAGE_WIDTH - 2 * MARGIN
avg_char_width = TEXT_FONT_SIZE * 0.45  # Approximate average character width
chars_per_line = int(usable_width / avg_char_width)

wrapper = textwrap.TextWrapper(width=chars_per_line)
lines = []
for para in body_text.split('\n'):
    lines.extend(wrapper.wrap(para))
    lines.append('')  # Blank line between paragraphs

lines_per_page = int((PAGE_HEIGHT - 2 * MARGIN) / LINE_HEIGHT)
chunks = [lines[i:i + lines_per_page] for i in range(0, len(lines), lines_per_page)]

# --- Add content pages ---
for i, chunk in enumerate(chunks):
    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    y = MARGIN
    for line in chunk:
        text_rect = fitz.Rect(MARGIN, y, PAGE_WIDTH - MARGIN, y + LINE_HEIGHT)
        page.insert_text((MARGIN, y), line, fontname="helv", fontsize=TEXT_FONT_SIZE, color=(0.1, 0.1, 0.1))
        page.draw_rect(text_rect, color=(0, 0, 1), width=0.5)  # Blue border around each line
        y += LINE_HEIGHT
    # Page number (bottom center)
    page_num_rect = fitz.Rect(PAGE_WIDTH / 2 - 20, PAGE_HEIGHT - 40, PAGE_WIDTH / 2 + 20, PAGE_HEIGHT - 20)
    page.insert_textbox(page_num_rect, str(i + 1), fontname="helv", fontsize=10, align=1, color=(0.2, 0.2, 0.2))
    page.draw_rect(page_num_rect, color=(0, 0, 0), width=0.5)  # Black border

# Save the final PDF
output_filename = "ebook_layout.pdf"
doc.save(output_filename)
doc.close()
