import fitz  # PyMuPDF

def create_pocketmod_layout(input_pdf_path, output_pdf_path):
    input_pdf = fitz.open(input_pdf_path)
    pocketmod_pdf = fitz.open()

    full_width, full_height = 612, 792  # US Letter size in points
    page_width, page_height = full_width / 2, full_height / 4

    sheet = pocketmod_pdf.new_page(width=full_width, height=full_height)
    layout_order = [4, 5, 6, 7, 2, 1, 0, 3]

    # Ensure we have at least 8 pages
    while len(input_pdf) < 8:
        input_pdf.insert_pdf(input_pdf, from_page=0, to_page=0)

    for i, page_index in enumerate(layout_order):
        src_page = input_pdf[page_index]
        pix = src_page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))  # scale to fit
        img_rect = fitz.Rect(
            (i % 2) * page_width,
            (i // 2) * page_height,
            (i % 2 + 1) * page_width,
            (i // 2 + 1) * page_height
        )
        sheet.insert_image(img_rect, pixmap=pix)

        # Draw red rectangle to show page edges
        sheet.draw_rect(img_rect, color=(1, 1, 0), width=1)

    pocketmod_pdf.save(output_pdf_path)
    pocketmod_pdf.close()
    input_pdf.close()

# Example usage
create_pocketmod_layout("example.pdf", "pocketmod_output.pdf")
