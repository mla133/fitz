import pymupdf

def impose_zine_layout(input_pdf_path, output_pdf_path):
    """
    Arranges an 8-page PDF for printing as a single-sheet, double-sided zine.
    
    Each side of a landscape letter sheet holds four pages; the top row is
    printed upside down so the pages read correctly after folding:
    Side 1: top [Page 5, Page 4] (rotated 180), bottom [Page 8, Page 1]
    Side 2: top [Page 3, Page 6] (rotated 180), bottom [Page 2, Page 7]

    Print double-sided, flipping on the short edge. Fold the top half down
    behind the bottom, then fold in half so Page 1 is the front cover.

    The script assumes the input is an 8-page PDF.
    """
    input_doc = pymupdf.open(input_pdf_path)
    if input_doc.page_count != 8:
        raise ValueError(f"Expected an 8-page PDF, got {input_doc.page_count} pages.")
    output_doc = pymupdf.open()

    # Landscape US letter (11 x 8.5 inches)
    sheet_width = 11 * 72
    sheet_height = 8.5 * 72
    half_width = sheet_width / 2
    half_height = sheet_height / 2

    top_left = pymupdf.Rect(0, 0, half_width, half_height)
    top_right = pymupdf.Rect(half_width, 0, sheet_width, half_height)
    bottom_left = pymupdf.Rect(0, half_height, half_width, sheet_height)
    bottom_right = pymupdf.Rect(half_width, half_height, sheet_width, sheet_height)

    # 0-based page indexes: (top_left, top_right, bottom_left, bottom_right)
    sides = [
        (4, 3, 7, 0),  # Side 1: pages 5, 4 / 8, 1
        (2, 5, 1, 6),  # Side 2: pages 3, 6 / 2, 7
    ]

    for tl, tr, bl, br in sides:
        # A new_page() call invalidates previously returned page objects,
        # so each sheet is fully populated before the next is created.
        sheet = output_doc.new_page(width=sheet_width, height=sheet_height)
        sheet.show_pdf_page(top_left, input_doc, tl, rotate=180)
        sheet.show_pdf_page(top_right, input_doc, tr, rotate=180)
        sheet.show_pdf_page(bottom_left, input_doc, bl)
        sheet.show_pdf_page(bottom_right, input_doc, br)

    output_doc.save(output_pdf_path)
    output_doc.close()
    input_doc.close()
    print(f"Imposed zine saved to '{output_pdf_path}'.")

# Example usage
impose_zine_layout("zine_with_content.pdf", "zine_imposed_for_print.pdf")
