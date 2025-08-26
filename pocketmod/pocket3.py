import fitz  # PyMuPDF

def create_pocketmod_pdf(output_pdf_path):
    pocketmod_pdf = fitz.open()

    full_width, full_height = 612, 792  # US Letter size
    page_width, page_height = full_width / 2, full_height / 4

    sheet = pocketmod_pdf.new_page(width=full_width, height=full_height)

    # PocketMod layout order and rotation angles for correct folding
    layout_order = [
        (1, 90),  # top-left
        (0, 270),  # top-right
        (2, 90),  # second row left
        (7, 270),  # second row right
        (3, 90),    # third row left
        (6, 270),    # third row right
        (4, 90),    # bottom-left
        (5, 270)     # bottom-right
    ]

    # Generate 8 portrait-oriented pages with sample content
    sample_pages = []
    for i in range(8):
        temp_doc = fitz.open()
        temp_page = temp_doc.new_page(width=page_height, height=page_width)  # portrait layout
        temp_page.insert_text(
            fitz.Point(72, 72),
            f"Page {i+1}",
            fontsize=30
        )
        sample_pages.append(temp_page)

    # Place each page into the correct position on the PocketMod sheet
    for i, (page_index, rotation) in enumerate(layout_order):
        src_page = sample_pages[page_index]
        rotate_matrix = fitz.Matrix(1, 1).prerotate(rotation)
        pix = src_page.get_pixmap(matrix=rotate_matrix)
        img_rect = fitz.Rect(
            (i % 2) * page_width,
            (i // 2) * page_height,
            (i % 2 + 1) * page_width,
            (i // 2 + 1) * page_height
        )
        sheet.insert_image(img_rect, pixmap=pix)
        sheet.draw_rect(img_rect, color=(1, 0, 0), width=1)  # red border

    pocketmod_pdf.save(output_pdf_path)
    pocketmod_pdf.close()

# Generate the PocketMod PDF
create_pocketmod_pdf("pocketmod_output.pdf")
