# Generates a pocketmod PDF from 'example.pdf', or generates
# a generic layout example if no input PDF given

import fitz  # PyMuPDF

def create_pocketmod_pdf(output_path='pocketmod_output.pdf', input_pdf_path=None):
    # Define page and mini-page dimensions
    page_width, page_height = 612, 792  # US Letter size in points
    mini_width, mini_height = page_width / 2, page_height / 4

    # Create a new blank PDF document
    doc = fitz.open()
    page = doc.new_page(width=page_width, height=page_height)

    # Define layout order: (page_index, rotation)
    layout_order = [
        (1, 90),   # top-left
        (0, 270),  # top-right
        (2, 90),   # second row left
        (7, 270),  # second row right
        (3, 90),   # third row left
        (6, 270),  # third row right
        (4, 90),   # bottom-left
        (5, 270)   # bottom-right
    ]

    # Load input PDF if provided
    input_pages = []
    if input_pdf_path:
        input_doc = fitz.open(input_pdf_path)
        input_pages = [input_doc.load_page(i) for i in range(min(len(input_doc), 8))]

    # Place each mini-page
    for i, (pos_index, rotation) in enumerate(layout_order):
        # Calculate position
        col = pos_index % 2
        row = pos_index // 2
        x0 = col * mini_width
        y0 = row * mini_height
        rect = fitz.Rect(x0, y0, x0 + mini_width, y0 + mini_height)

        # Create mini-page content
        if input_pages:
            # Use content from input PDF
            page.show_pdf_page(rect, input_pages[i].parent, input_pages[i].number, rotate=rotation)
        else:
            # Generate dummy content
            shape = page.new_shape()
            shape.draw_rect(rect)
            shape.finish(color=(1, 0, 0), fill=None)  # Red border
            text = f"Page {i + 1}"
            page.insert_textbox(rect, text, fontsize=80, rotate=rotation, align=1)

        img_rect = fitz.Rect(
            (i % 2) * page_width,
            (i // 2) * page_height,
            (i % 2 + 1) * page_width,
            (i // 2 + 1) * page_height
        )
        # Draw red rectangle to show page edges
        page.draw_rect(img_rect, color=(0, 0, 0), width=1)

    # Save the final PDF
    doc.save(output_path)
    doc.close()

# Example usage:
#create_pocketmod_pdf()  # Generates dummy content
create_pocketmod_pdf(input_pdf_path='example.pdf')  # Uses pages from example.pdf
