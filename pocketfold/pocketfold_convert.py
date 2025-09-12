import fitz  # PyMuPDF

example_pdf = 'fontsizes.pdf'

def create_pocketfold_pdf(output_path='pocketfold_output.pdf', input_pdf_path=None):
    page_width, page_height = 612, 792  # US Letter size
    mini_width, mini_height = page_width / 2, page_height / 4

    doc = fitz.open()
    page = doc.new_page(width=page_width, height=page_height)

    # Correct PocketFold layout: (page_index, rotation)
    layout_order = [
        (3, 270),   # top-left
        (1, 90),  # top-right
        (4, 270),   # second row left
        (0, 90),  # second row right
        (5, 270),   # third row left
        (7, 90),  # third row right
        (6, 270),   # bottom-left
        (2, 90)   # bottom-right
    ]
    input_pages = []
    if input_pdf_path:
        input_doc = fitz.open(input_pdf_path)
        input_pages = [input_doc.load_page(i) for i in range(min(len(input_doc), 8))]

    for i, (page_index, rotation) in enumerate(layout_order):
        col = i % 2
        row = i // 2
        x0 = col * mini_width
        y0 = row * mini_height
        rect = fitz.Rect(x0, y0, x0 + mini_width, y0 + mini_height)

        if input_pages:
            page.show_pdf_page(rect, input_pages[page_index].parent, input_pages[page_index].number, rotate=rotation)
        else:
            shape = page.new_shape()
            shape.draw_rect(rect)
            shape.finish(color=(1, 0, 0), fill=None)
            text = f"Page {page_index + 1}"
            page.insert_textbox(rect, text, fontsize=80, rotate=rotation, align=1)

        page.draw_rect(rect, color=(0, 0, 0), width=1)

    # Add horizontal line between mini pages 5 & 6 (rows 2 and 3)
    cut_y = page_height / 2
    cut_line_thickness = 0.5
    cut_color = (0, 1, 0) # Green(?)
    x_start = 0 * mini_width
    x_end = 1 * mini_width
    cut_line = fitz.Rect(0, cut_y, x_end, cut_y + cut_line_thickness)
    page.draw_rect(cut_line, color=cut_color, width=cut_line_thickness)

    doc.save(output_path)
    doc.close()

# Example usage:
#create_pocketfold_pdf()  # Dummy layout
create_pocketfold_pdf(input_pdf_path=example_pdf)  # From input PDF
