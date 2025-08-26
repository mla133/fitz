import fitz  # PyMuPDF

#####  Documentation methods #####
# See all available methods and attributes
#print(dir(fitz))
# Explore a specific class, like Document or Page
#print(dir(fitz.Document))
#print(dir(fitz.Page))
#help(fitz.Page)
#exit()      # used to break the script early

# Define dimensions for the mint tin template in millimeters
width_mm = 95
height_mm = 60

# Convert millimeters to points (1 mm = 2.83465 points)
width_pt = width_mm * 2.83465
height_pt = height_mm * 2.83465

# Create a new PDF document
doc = fitz.open()

# Add a page with the specified dimensions
page = doc.new_page(width=width_pt, height=height_pt)

# Define margins and layout
margin = 5 * 2.83465  # 5mm margin in points
title_text = "Mint Tin Label Template"
sample_text = "This is a sample content block for your mint tin design."

# Draw decorative border
rect = fitz.Rect(margin, margin, width_pt - margin, height_pt - margin)
page.draw_rect(rect, color=(0, 0, 0), width=1)

# Add title at the top center using approximate centering
title_font_size = 14
title_x = width_pt / 2 - 100  # approximate centering
title_y = margin + 10
page.insert_text((title_x, title_y), title_text, fontsize=title_font_size, fontname="helv", fill=(0, 0, 0))

# Add sample text block in the center using approximate centering
sample_font_size = 10
sample_x = width_pt / 2 - 120  # approximate centering
sample_y = height_pt / 2
page.insert_text((sample_x, sample_y), sample_text, fontsize=sample_font_size, fontname="helv", fill=(0, 0, 0))

# Save the populated PDF
output_file = "mint_tin_template_populated.pdf"
doc.save(output_file)
doc.close()

# Testing to see if I can read the extracted text from the newly created file
check_file = "ebook.pdf" 
doc = fitz.open(check_file)
page = doc[0]
text = page.get_text()  # Extract all text
print(text)
doc.close()



"""
===========================
PyMuPDF (fitz) Cheat Sheet
===========================

Basic Setup
-----------
import fitz  # PyMuPDF

doc = fitz.open("file.pdf")  # Open existing PDF
page = doc[0]                # Access first page
doc.save("new_file.pdf")     # Save changes

Creating a New PDF
------------------
doc = fitz.open()
page = doc.new_page(width=595, height=842)  # A4 size in points
doc.save("blank.pdf")

Inserting Text
--------------
page.insert_text((100, 100), "Hello World", fontsize=12, fontname="helv", fill=(0, 0, 0))

Inserting Images
----------------
rect = fitz.Rect(50, 50, 200, 200)
page.insert_image(rect, filename="image.png")

Drawing Shapes
--------------
rect = fitz.Rect(50, 50, 300, 150)
page.draw_rect(rect, color=(1, 0, 0), width=2)  # Red border
page.draw_circle((150, 100), radius=40, color=(0, 0, 1))  # Blue circle

Extracting Content
------------------
text = page.get_text()  # Extract all text
words = page.get_text("words")  # Get words with positions
images = page.get_images()  # List of images on the page

Working with Annotations
------------------------
annot = page.add_text_annot((100, 100), "Note here")
annot.set_info(title="Author", subject="Comment")

Working with Coordinates
------------------------
- All positions are in points (1 point = 1/72 inch).
- Convert mm to points: mm * 2.83465

Removing Content
----------------
page.delete_text()  # Remove all text
page.delete_annot(annot)  # Remove specific annotation

Document Info
-------------
info = doc.metadata
print(info["title"], info["author"])
"""
