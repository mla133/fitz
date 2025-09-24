import fitz

def impose_zine_layout(input_pdf_path, output_pdf_path):
    """
    Arranges an 8-page PDF for printing as a single-sheet, double-sided zine.
    
    The imposition order for an 8-page single-sheet zine is:
    Side 1: [Page 8, Page 1] and [Page 4, Page 5]
    Side 2: [Page 6, Page 3] and [Page 2, Page 7]
    
    The script assumes the input is an 8-page PDF (0-indexed).
    """
    input_doc = fitz.open(input_pdf_path)
    output_doc = fitz.open()

    # The imposition requires two new pages in the output document
    # for double-sided printing. The new pages will be standard letter size (8.5x11).
    page_width = 8.5 * 72
    page_height = 11 * 72

    # Create first output page for the front and back covers (folded side)
    output_page1 = output_doc.new_page(width=page_height, height=page_width)
    
    # Create second output page for the interior pages
    output_page2 = output_doc.new_page(width=page_height, height=page_width)

    # Define the four quadrants for each letter-size page
    half_width = page_height / 2
    half_height = page_width / 2
    
    # Quadrant rectangles on the output page
    top_left = fitz.Rect(0, 0, half_width, half_height)
    top_right = fitz.Rect(half_width, 0, page_height, half_height)
    bottom_left = fitz.Rect(0, half_height, half_width, page_width)
    bottom_right = fitz.Rect(half_width, half_height, page_height, page_width)
    
    # Side 1: pages 8, 1, 4, 5
    # Pages 8 and 1 are placed on the front page, side-by-side
    # The rect for page 8 (index 7) needs to be rotated and placed on the right.
    # The rect for page 1 (index 0) is placed on the left.
    output_page1.show_pdf_page(top_left, input_doc, 0)
    output_page1.show_pdf_page(top_right, input_doc, 7, matrix=fitz.Matrix(0, 1, -1, 0))

    # Pages 4 and 5 are on the bottom, but in a different orientation
    output_page1.show_pdf_page(bottom_left, input_doc, 4)
    output_page1.show_pdf_page(bottom_right, input_doc, 3, matrix=fitz.Matrix(0, 1, -1, 0))
    
    # Side 2: pages 6, 3, 2, 7
    # Pages 6 and 3
    output_page2.show_pdf_page(top_left, input_doc, 5)
    output_page2.show_pdf_page(top_right, input_doc, 2, matrix=fitz.Matrix(0, 1, -1, 0))
    
    # Pages 2 and 7
    output_page2.show_pdf_page(bottom_left, input_doc, 1)
    output_page2.show_pdf_page(bottom_right, input_doc, 6, matrix=fitz.Matrix(0, 1, -1, 0))

    output_doc.save(output_pdf_path)
    output_doc.close()
    input_doc.close()
    print(f"Imposed zine saved to '{output_pdf_path}'.")

# Example usage
impose_zine_layout("zine_with_content.pdf", "zine_imposed_for_print.pdf")
