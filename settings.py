import fitz  # PyMuPDF

# Define portrait letter-size page dimensions in points
page_width = 612  # Letter width in points
page_height = 792  # Letter height in points

# Define margins in points
margin_left = 50
margin_right = 50
margin_top = 50
margin_bottom = 50

# Create a new PDF document
doc = fitz.open()

# Add a page with specified dimensions
page = doc.new_page(width=page_width, height=page_height)

# Draw margin lines in red
page.draw_line((margin_left, 0), (margin_left, page_height), color=(1, 0, 0))
page.draw_line((page_width - margin_right, 0), (page_width - margin_right, page_height), color=(1, 0, 0))
page.draw_line((0, margin_top), (page_width, margin_top), color=(1, 0, 0))
page.draw_line((0, page_height - margin_bottom), (page_width, page_height - margin_bottom), color=(1, 0, 0))

# Draw grid lines inside the margin area (every 50 points)
grid_spacing = 50
for x in range(margin_left + grid_spacing, page_width - margin_right, grid_spacing):
    page.draw_line((x, margin_top), (x, page_height - margin_bottom), color=(0.7, 0.7, 0.7))
for y in range(margin_top + grid_spacing, page_height - margin_bottom, grid_spacing):
    page.draw_line((margin_left, y), (page_width - margin_right, y), color=(0.7, 0.7, 0.7))

# Prepare settings text
settings_text = f"""Page Size: {page_width} x {page_height} points (Letter Portrait)
Margins:
  Left: {margin_left} pts
  Right: {margin_right} pts
  Top: {margin_top} pts
  Bottom: {margin_bottom} pts
Layout:
  Margin lines: Red
  Grid lines: Every {grid_spacing} pts (Gray)
  Header/Footer: Present
Header:
  Left: {margin_left} pts (margin_left)
  Top:  {margin_top-40} pts (margin_top-40)
Footer:
  Left: {margin_left} pts (margin_left)
  Bottom: {page_height - margin_bottom + 20} pts (page_height - margin_bottom + 20)
  """

# Add header text
page.insert_text((margin_left, margin_top - 40), "Header: Document Layout Settings", fontsize=12, color=(0, 0, 0))

# Add footer text
page.insert_text((margin_left, page_height - margin_bottom + 20), "Footer: End of Layout Page", fontsize=12, color=(0, 0, 0))

# Add settings text inside the margin area
page.insert_text((margin_left + 10, margin_top + 10), settings_text, fontsize=12, color=(0, 0, 0))

# Save the PDF
output_file = "pdf_with_letter_margins_grid_header_footer.pdf"
doc.save(output_file)
doc.close()
