import fitz  # PyMuPDF
import random

# Create a new PDF document
doc = fitz.open()

# Create a new page
page = doc.new_page()

# Define dice types and their maximum values
dice_types = {
    "1d4": 4,
    "1d6": 6,
    "1d8": 8,
    "1d10": 10,
    "1d12": 12,
    "1d20": 20,
    "1d100": 100
}

# Roll each die
dice_results = {die: random.randint(1, max_val) for die, max_val in dice_types.items()}

# Layout parameters
font_size = 28
margin = 72
spacing_y = 50
page_width, page_height = fitz.paper_size("a4")

# Insert title
page.insert_text((margin, margin), "Dice Roller Results", fontsize=font_size + 4, fontname="helv", fill=(0, 0, 0))

# Insert each die result
y_position = margin + 60
for die, result in dice_results.items():
    text = f"{die}: {result}"
    page.insert_text((margin, y_position), text, fontsize=font_size, fontname="helv", fill=(0, 0, 0))
    y_position += spacing_y

# Save the PDF
output_file = "dice_roller_results.pdf"
doc.save(output_file)
doc.close()
