import fitz  # PyMuPDF
import textwrap

def render_paragraphs_to_pdf_with_margins(
    text,
    output_file="formatted_paragraphs_with_margins.pdf",
    page_width=595,
    page_height=842,
    left_margin=50,
    top_margin=50,
    right_margin=50,
    bottom_margin=50,
    font_size=12,
    font_name="helv",
    line_spacing=1.5,
    wrap_width=80
):
    """
    Renders a long string with multiple paragraphs into a PDF with proper spacing and wrapping,
    and includes visible margin lines on all four sides.
    """
    # Create a new PDF document
    doc = fitz.open()
    page = doc.new_page(width=page_width, height=page_height)

    # Calculate usable width and line height
    usable_width = page_width - left_margin - right_margin
    line_height = font_size * line_spacing
    y = top_margin

    # Draw margin lines
    margin_color = (0.5, 0.5, 0.5)  # Gray color
    page.draw_line((left_margin, top_margin), (left_margin, page_height - bottom_margin), color=margin_color)
    page.draw_line((page_width - right_margin, top_margin), (page_width - right_margin, page_height - bottom_margin), color=margin_color)
    page.draw_line((left_margin, top_margin), (page_width - right_margin, top_margin), color=margin_color)
    page.draw_line((left_margin, page_height - bottom_margin), (page_width - right_margin, page_height - bottom_margin), color=margin_color)

    # Split text into paragraphs
    paragraphs = text.split("\n")

    for para in paragraphs:
        # Wrap paragraph text
        wrapped_lines = textwrap.wrap(para, width=wrap_width)
        for line in wrapped_lines:
            if y + line_height > page_height - bottom_margin:
                # Add new page if current page is full
                page = doc.new_page(width=page_width, height=page_height)
                y = top_margin
                # Draw margin lines on new page
                page.draw_line((left_margin, top_margin), (left_margin, page_height - bottom_margin), color=margin_color)
                page.draw_line((page_width - right_margin, top_margin), (page_width - right_margin, page_height - bottom_margin), color=margin_color)
                page.draw_line((left_margin, top_margin), (page_width - right_margin, top_margin), color=margin_color)
                page.draw_line((left_margin, page_height - bottom_margin), (page_width - right_margin, page_height - bottom_margin), color=margin_color)
            page.insert_text((left_margin, y), line, fontsize=font_size, fontname=font_name, fill=(0, 0, 0))
            y += line_height
        y += line_height  # Extra space between paragraphs

    # Save the PDF
    doc.save(output_file)
    doc.close()

# Example usage
sample_text = """This is the first paragraph. It contains multiple sentences and should wrap nicely within the page margins.
This is the second paragraph. It follows the first and should be spaced properly.
Here is a third paragraph that is a bit longer and will likely wrap across multiple lines depending on the width setting."""

render_paragraphs_to_pdf_with_margins(sample_text)
