import fitz  # PyMuPDF
import textwrap

def render_paragraphs_to_pdf(
    text,
    output_file="formatted_paragraphs.pdf",
    page_width=612,
    page_height=792,
    left_margin=36,
    top_margin=36,
    right_margin=36,
    bottom_margin=36,
    font_size=12,
    font_name="helv",
    line_spacing=1.5,
    wrap_width=100
):
    """
    Renders a long string with multiple paragraphs into a PDF with proper spacing and wrapping.
    """
    # Create a new PDF document
    doc = fitz.open()
    page = doc.new_page(width=page_width, height=page_height)

    # Calculate usable width and line height
    usable_width = page_width - left_margin - right_margin
    line_height = font_size * line_spacing
    y = top_margin

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

render_paragraphs_to_pdf(sample_text)
