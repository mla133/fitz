import fitz  # PyMuPDF

def create_zine(image_paths, text_content, output_file):
    """
    Generates a foldable four-page zine layout on a single A4 sheet.

    :param image_paths: A list of file paths to the images for each page.
    :param text_content: A list of text strings for each page.
    :param output_file: The name of the output PDF file.
    """
    doc = fitz.open()  # Create a new PDF document
    page = doc.new_page(width=fitz.paper_size("a4")[0], height=fitz.paper_size("a4")[1])

    # A4 dimensions in points (approx. 595 x 842)
    page_width = page.rect.width
    page_height = page.rect.height

    # Coordinates for the four quadrants of the A4 page
    # Top-right corner for Zine Page 1
    rect_p1 = fitz.Rect(page_width / 2, 0, page_width, page_height / 2)
    # Top-left corner for Zine Page 2
    rect_p2 = fitz.Rect(0, 0, page_width / 2, page_height / 2)
    # Bottom-left corner for Zine Page 3
    rect_p3 = fitz.Rect(0, page_height / 2, page_width / 2, page_height)
    # Bottom-right corner for Zine Page 4
    rect_p4 = fitz.Rect(page_width / 2, page_height / 2, page_width, page_height)

    # Optional: Draw a grid to visualize the layout
    # This helps confirm placement during testing.
    page.draw_rect(rect_p1, color=(0, 0, 0), width=0.5)
    page.draw_rect(rect_p2, color=(0, 0, 0), width=0.5)
    page.draw_rect(rect_p3, color=(0, 0, 0), width=0.5)
    page.draw_rect(rect_p4, color=(0, 0, 0), width=0.5)

    # Place content on the respective page rectangles
    # Insert images
    page.insert_image(rect_p1, filename=image_paths[0])  # Cover
    page.insert_image(rect_p2, filename=image_paths[1])  # Inside back cover
    page.insert_image(rect_p3, filename=image_paths[2])  # Inside front cover
    page.insert_image(rect_p4, filename=image_paths[3])  # Back cover

    # Insert text (e.g., as captions)
    page.insert_textbox(rect_p1, text_content[0], fontname="helv", fontsize=10)
    page.insert_textbox(rect_p2, text_content[1], fontname="helv", fontsize=10)
    page.insert_textbox(rect_p3, text_content[2], fontname="helv", fontsize=10)
    page.insert_textbox(rect_p4, text_content[3], fontname="helv", fontsize=10)
    
    # Save the final PDF
    doc.save(output_file)
    doc.close()

# --- Example Usage ---
# You would need to have these files ready in your directory.
# images = ["cover_art.png", "page_2_image.png", "page_3_image.png", "page_4_image.png"]
images = ["map7.png", "map7.png", "map7.png", "map7.png"]
text = [
    "A cool zine cover!",
    "This is the left-hand page of the inside spread.",
    "This is the right-hand page of the inside spread.",
    "Back cover info or art."
]

# Assuming images and text lists are already populated with your content.
# If you don't have images, you can create dummy ones or omit them.
create_zine(images, text, "my_zine_layout.pdf")
