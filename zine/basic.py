import fitz

def create_zine_pages(output_path, num_pages=8):
    """Creates a new PDF with empty pages for a zine."""
    doc = fitz.open()  # Create new empty document
    # Set dimensions for a half-letter page (5.5 x 8.5 inches)
    half_letter_width = 5.5 * 72  # 72 points per inch
    half_letter_height = 8.5 * 72
    half_letter_rect = fitz.Rect(0, 0, half_letter_width, half_letter_height)
    
    for i in range(num_pages):
        # Insert pages with the specified dimensions
        doc.new_page(width=half_letter_width, height=half_letter_height)
        # Add a placeholder for demonstration
        page = doc[i]
        page.insert_text(fitz.Point(30, 30), f"Page {i + 1}", fontsize=18)
        
    doc.save(output_path)
    doc.close()
    print(f"Created a basic {num_pages}-page PDF at '{output_path}'.")

create_zine_pages("basic_zine.pdf")
