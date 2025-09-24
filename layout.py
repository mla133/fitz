import fitz  # PyMuPDF

# Create a new PDF document
doc = fitz.open()

# Add a new page (A5 size is common for eBooks)
page = doc.new_page(width=420, height=595)  # width, height in points

# Define content
title = "The Art of Python"
author = "Matthew Allen"
body = (
    "Python is a versatile programming language loved by developers worldwide. "
    "Its clear syntax and powerful libraries make it ideal for everything from web development "
    "to data science and artificial intelligence. This eBook explores Python's strengths, "
    "best practices, and practical examples to help you master the language."
)

# Define positions and styles
margin = 40
width = page.rect.width - 2 * margin

# Title
title_fontsize = 22
title_rect = fitz.Rect(margin, 60, margin + width, 100)
page.insert_textbox(
    title_rect, title,
    fontname="helv", fontsize=title_fontsize,
    align=1  # Centered
)

# Author
author_fontsize = 14
author_rect = fitz.Rect(margin, 105, margin + width, 130)
page.insert_textbox(
    author_rect, f"by {author}",
    fontname="helv", fontsize=author_fontsize,
    color=(0.3, 0.3, 0.3),
    align=1  # Centered
)

# Horizontal line separator
line_y = 140
page.draw_line(
    p1=(margin, line_y),
    p2=(margin + width, line_y),
    color=(0.7, 0.7, 0.7),
    width=1
)

# Body text
body_fontsize = 12
body_rect = fitz.Rect(margin, line_y + 20, margin + width, 500)
page.insert_textbox(
    body_rect, body,
    fontname="helv", fontsize=body_fontsize,
    align=4  # Justified
)

# Page number (bottom center)
page_number = 1
page_num_fontsize = 10
page_num_text = f"{page_number}"
page_num_rect = fitz.Rect(
    page.rect.width / 2 - 20, page.rect.height - 40,
    page.rect.width / 2 + 20, page.rect.height - 20
)
page.insert_textbox(
    page_num_rect, page_num_text,
    fontname="helv", fontsize=page_num_fontsize,
    align=1  # Centered
)

# Save the PDF
doc.save("ebook_sample_page.pdf")
doc.close()
