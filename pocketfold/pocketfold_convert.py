import fitz  # PyMuPDF

def create_pocketfold_pdf(output_path='pocketfold_output.pdf', input_pdf_path=None):
    page_width, page_height = 612, 792  # US Letter size
    mini_width, mini_height = page_width / 2, page_height / 4
    half_height = page_height / 2

    doc = fitz.open()

    # Load input pages if provided
    input_pages = []
    if input_pdf_path:
        input_doc = fitz.open(input_pdf_path)
        input_pages = [input_doc.load_page(i) for i in range(len(input_doc))]

    # First page: 8 mini-pages
    page1 = doc.new_page(width=page_width, height=page_height)
    layout_order = [
        (3, 270), (1, 90),
        (4, 270), (0, 90),
        (5, 270), (7, 90),
        (6, 270), (2, 90)
    ]

    for i, (page_index, rotation) in enumerate(layout_order):
        col = i % 2
        row = i // 2
        x0 = col * mini_width
        y0 = row * mini_height
        rect = fitz.Rect(x0, y0, x0 + mini_width, y0 + mini_height)

        if input_pages and page_index < len(input_pages):
            page1.show_pdf_page(rect, input_pages[page_index].parent, input_pages[page_index].number, rotate=rotation)
        else:
            shape = page1.new_shape()
            shape.draw_rect(rect)
            shape.finish(color=(1, 0, 0), fill=None)
            text = f"Page {page_index + 1}"
            page1.insert_textbox(rect, text, fontsize=80, rotate=rotation, align=1)

        page1.draw_rect(rect, color=(0, 0, 0), width=1)

    # Add horizontal cut line between mini pages 5 & 6 (rows 2 and 3)
    cut_line_thickness = 0.5
    cut_color = (0, 1, 0)
    cut_line = fitz.Rect(0, page_height / 2, page_width / 2, (page_height / 2) + cut_line_thickness)
    page1.draw_rect(cut_line, color=cut_color, width=cut_line_thickness)

    # Second page: 2 half-pages
    page2 = doc.new_page(width=page_width, height=page_height)
    half_page_order = [
        (8, 270),  # top half
        (9, 270)   # bottom half
    ]
    for i, (page_index, rotation) in enumerate(half_page_order):
        x0 = 0
        y0 = i * half_height
        rect = fitz.Rect(x0, y0, x0 + page_width, y0 + half_height)

        if input_pages and page_index < len(input_pages):
            page2.show_pdf_page(rect, input_pages[page_index].parent, input_pages[page_index].number, rotate=rotation)
        else:
            shape = page2.new_shape()
            shape.draw_rect(rect)
            shape.finish(color=(0, 0, 1), fill=None)
            text = f"Page {page_index + 1}"
            page2.insert_textbox(rect, text, fontsize=36, rotate=rotation, align=1)

        page2.draw_rect(rect, color=(0, 0, 0), width=1)

    doc.save(output_path)
    doc.close()

# Example usage:
#create_pocketfold_pdf()  # Dummy layout
create_pocketfold_pdf(input_pdf_path='generated_document.pdf')  # From input PDF
