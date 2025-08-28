import fitz  # PyMuPDF

def create_business_card_layout_with_visible_borders(output_path='business_cards_with_borders.pdf'):
    # US Letter size in points
    page_width, page_height = 612, 792

    # Business card size in points (3.5 x 2 inches)
    card_width, card_height = 252, 144

    # Calculate number of cards that fit horizontally and vertically
    cols = page_width // card_width
    rows = page_height // card_height
    max_cards = int(cols * rows)

    # Create a new blank PDF document
    doc = fitz.open()
    page = doc.new_page(width=page_width, height=page_height)

    # Placeholder text and logo dimensions
    placeholder_text = "John Doe\nDeveloper"
    logo_rect_height = 40
    logo_rect_width = 40

    # Place each business card
    for i in range(max_cards):
        col = i % int(cols)
        row = i // int(cols)
        x0 = col * card_width
        y0 = row * card_height
        rect = fitz.Rect(x0, y0, x0 + card_width, y0 + card_height)

        # Draw card border directly on the page
        page.draw_rect(rect, color=(0, 0, 1), width=1)  # Blue border

        # Insert placeholder text
        page.insert_textbox(rect, placeholder_text, fontsize=12, align=1)

        # Draw placeholder logo as a gray square
        logo_x0 = x0 + 10
        logo_y0 = y0 + 10
        logo_rect = fitz.Rect(logo_x0, logo_y0, logo_x0 + logo_rect_width, logo_y0 + logo_rect_height)
        page.draw_rect(logo_rect, color=(0.5, 0.5, 0.5), fill=(0.8, 0.8, 0.8))

        # Label the logo area
        page.insert_textbox(logo_rect, "Logo", fontsize=8, align=1)

    # Save the final PDF
    doc.save(output_path)
    doc.close()

# Generate the business card layout with visible borders
create_business_card_layout_with_visible_borders()
