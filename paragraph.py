import fitz  # PyMuPDF
import textwrap

doc = fitz.open()
page = doc.new_page(width=595, height=842)  # A4 size

text = """This is a long paragraph that should wrap nicely within the page.
Here's another paragraph that follows the first one. It should be spaced properly."""

# Settings
left_margin = 50
top_margin = 50
max_width = 495  # page width - margins
font_size = 12
line_height = font_size * 1.5

# Split into paragraphs
paragraphs = text.split("\n")
y = top_margin

for para in paragraphs:
    # Wrap text to fit within max_width
    wrapped = textwrap.wrap(para, width=80)  # Adjust width based on font and page size
    for line in wrapped:
        page.insert_text((left_margin, y), line, fontsize=font_size)
        y += line_height
    y += line_height  # Extra space between paragraphs

doc.save("paragraphs.pdf")
doc.close()
