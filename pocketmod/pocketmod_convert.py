import fitz  # PyMuPDF

example_pdf = 'fontsizes.pdf'

def create_pocketmod_pdf(output_path='pocketmod_output.pdf', input_pdf_path=None):
    page_width, page_height = 612, 792  # US Letter size
    mini_width, mini_height = page_width / 2, page_height / 4

    doc = fitz.open()
    page = doc.new_page(width=page_width, height=page_height)

    # Correct PocketMod layout: (page_index, rotation)
    layout_order = [
        (5, 270),   # top-left
        (4, 90),  # top-right
        (6, 270),   # second row left
        (3, 90),  # second row right
        (7, 270),   # third row left
        (2, 90),  # third row right
        (0, 270),   # bottom-left
        (1, 90)   # bottom-right
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

    # Add vertical cut line between mini pages 3,4,7,8 (rows 2 and 3)
    cut_x = page_width / 2
    cut_line_thickness = 0.5
    cut_color = (1, 0, 0)  # Red
    y_start = 1 * mini_height
    y_end = 3 * mini_height
    cut_line = fitz.Rect(cut_x, y_start, cut_x + cut_line_thickness, y_end)
    page.draw_rect(cut_line, color=cut_color, width=cut_line_thickness)

    doc.save(output_path)
    doc.close()

# Example usage:
#create_pocketmod_pdf()  # Dummy layout
create_pocketmod_pdf(input_pdf_path=example_pdf)  # From input PDF
