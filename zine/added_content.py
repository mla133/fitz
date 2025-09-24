import fitz

def add_content_to_page(doc, page_number, title, body_text, image_path=None):
    """Adds a title, body text, and an image to a specific zine page."""
    page = doc.load_page(page_number)
    
    # Define coordinate system
    page_rect = page.rect
    
    # Add title text
    title_rect = fitz.Rect(page_rect.x0 + 20, page_rect.y0 + 20, page_rect.x1 - 20, page_rect.y0 + 80)
    page.insert_textbox(title_rect, title, fontsize=24, fontname="Helvetica-Bold", align=fitz.TEXT_ALIGN_CENTER)
    
    # Add body text
    text_rect = fitz.Rect(page_rect.x0 + 20, title_rect.y1 + 10, page_rect.x1 - 20, page_rect.y1 - 20)
    page.insert_textbox(text_rect, body_text, fontsize=12, fontname="Helvetica")

    # Add image if path is provided
    if image_path:
        image_rect = fitz.Rect(page_rect.x0 + 50, page_rect.y0 + 150, page_rect.x1 - 50, page_rect.y1 - 100)
        page.insert_image(image_rect, filename=image_path)
        
    # Add page number
    page_number_text = f"{page_number + 1}"
    page.insert_text(fitz.Point(page_rect.x1 - 30, page_rect.y1 - 20), page_number_text, fontsize=10)

# Example usage (assuming 'my_image.png' exists)
doc = fitz.open("basic_zine.pdf")
#  add_content_to_page(doc, 0, "My Zine Title", "This is the front cover.", "my_image.png")
add_content_to_page(doc, 0, "My Zine Title", "This is the front cover.")
doc.save("zine_with_content.pdf")
doc.close()
