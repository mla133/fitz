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
    page.insert_text((margin, margin), header_text, fontsize=font_size_header, fontname="Courier", fill=(0, 0, 0))
    # Insert body text
    page.insert_text((margin, margin + 60), body_text, fontsize=font_size_body, fontname="Courier", fill=(0, 0, 0))

# Page 9: Auto-generated rolls from 1 to 100 in grid format filling the page
page9 = doc.new_page()
d100_rolls = [random.randint(1, 100) for _ in range(400)]

# Calculate grid layout
cols = 20
rows = 20
usable_width = page_width - 2 * margin
usable_height = page_height - 2 * margin
cell_width = usable_width / cols
cell_height = usable_height / rows
pg9_header = f"Page 9 Header"

for idx, roll in enumerate(d100_rolls):
    row = idx // cols
    col = idx % cols
    x = margin + col * cell_width
    y = margin + row * cell_height
    d100_roll = f"{roll:02}" if roll < 100 else "00"

    # Insert header
    page9.insert_text((margin, margin), pg9_header, fontsize=font_size_header, fontname="Courier", fill=(0, 0, 0))

    # Insert body text
    page9.insert_text((x, y+60), str(d100_roll), fontsize=font_size_grid, fontname="Courier", fill=(0, 0, 0))

for idx, roll in enumerate(d100_rolls):
    row = idx // cols
    col = idx % cols
    x = margin +col * cell_width
    y = margin + row * cell_width


# Page 10: Simulated card draws
page10 = doc.new_page()
pg10_header = f"Page 10 Header"
page10.insert_text((margin, margin), "Page 10 Header", fontsize=font_size_header, fontname="Courier", fill=(0, 0, 0))

suits = ["S", "C", "H", "D"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
card_draws = [f"{random.choice(values)}{random.choice(suits)}" for _ in range(400)]

for idx, card in enumerate(card_draws):
    row = idx // cols
    col = idx % cols
    x = margin + col * cell_width
    y = margin + row * cell_height + 60
    if "H" in card:
        color = (1, 0, 0)
    elif "D" in card:
        color = (0, 1, 0)
    elif "S" in card:
        color = (0, 0, 1)
    elif "C":
        color = (0, 0, 0)

    #color = (1, 0, 0) if "H" in card or "D" in card else (0, 0, 0)

    page10.insert_text((x, y), card, fontsize=font_size_grid, fontname="Courier", fill=color)

# Save the PDF
output_file = "generated_document.pdf"
doc.save(output_file)
doc.close()
