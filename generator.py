import fitz  # PyMuPDF
import random

# Create a new PDF document
doc = fitz.open()

# Constants for layout
page_width, page_height = fitz.paper_size("a4")
margin = 72  # 1 inch margin
font_size_header = 36
font_size_body = 28
font_size_grid = 12 

# Add pages 1 to 8 with headers and body text
for i in range(1, 9):
    page = doc.new_page()
    header_text = f"Page {i} Header"
    body_text = f"This is the body text for page {i}."

    # Insert header
    page.insert_text((margin, margin), header_text, fontsize=font_size_header, fontname="helv", fill=(0, 0, 0))
    # Insert body text
    page.insert_text((margin, margin + 60), body_text, fontsize=font_size_body, fontname="helv", fill=(0, 0, 0))

# Page 9: Auto-generated rolls from 1 to 100 in grid format filling the page
page9 = doc.new_page()
rolls = [random.randint(1, 100) for _ in range(400)]

# Calculate grid layout
cols = 20
rows = 20
usable_width = page_width - 2 * margin
usable_height = page_height - 2 * margin
cell_width = usable_width / cols
cell_height = usable_height / rows
pg9_header = f"Page 9 Header"

for idx, roll in enumerate(rolls):
    row = idx // cols
    col = idx % cols
    x = margin + col * cell_width
    y = margin + row * cell_height
    formatted_roll = f"{roll:02}" if roll < 100 else "00"

    # Insert header
    page9.insert_text((margin, margin), pg9_header, fontsize=font_size_header, fontname="helv", fill=(0, 0, 0))

    # Insert body text
    page9.insert_text((x, y+60), str(formatted_roll), fontsize=font_size_grid, fontname="helv", fill=(0, 0, 0))

# Save the PDF
output_file = "generated_document.pdf"
doc.save(output_file)
doc.close()
