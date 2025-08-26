import fitz  # PyMuPDF

"""
📘 Markdown Simulation Guide for PyMuPDF (fitz)

PyMuPDF does not natively support Markdown, but you can simulate its formatting using font styles, sizes, and layout tricks.

1. Headers
   # Header 1 → fontsize=20
   ## Header 2 → fontsize=16
   ### Header 3 → fontsize=14
   Use bold font ("helvb") or underline if needed.

2. Bold and Italics
   **Bold** → fontname="helvb"
   *Italic* → fontname="helvi"

3. Bullet Lists
   - Item → use "•" symbol and indent (e.g., x + 20)
   Example: page.insert_text((x + 20, y), "• Item", fontsize=12)

4. Numbered Lists
   1. Item → manually number and indent
   Example: page.insert_text((x + 20, y), "1. Item", fontsize=12)

5. Code Blocks
   `code` or ```code``` → use monospaced font ("cour")
   Optional: draw a light gray rectangle behind the text
   Example:
     page.insert_text((x, y), "print('Hello')", fontname="cour")
     page.draw_rect(fitz.Rect(x, y, x + width, y + height), fill=(0.9, 0.9, 0.9))

6. Blockquotes
   > Quote → italic font, indent, optional vertical line
   Example:
     page.insert_text((x + 20, y), "Quote text", fontname="helvi")
     page.draw_line((x + 10, y), (x + 10, y + 20), color=(0.5, 0.5, 0.5))

7. Horizontal Rule
   --- → draw a horizontal line
   Example: page.draw_line((x, y), (x + width, y), color=(0.5, 0.5, 0.5))

8. Links
   text → display as plain text or underline
   Example: page.insert_text((x, y), "Google", fontsize=12, color=(0, 0, 1))

Note: All formatting must be manually applied. Markdown syntax is not interpreted by PyMuPDF.
"""

# Page dimensions
page_width = 612
page_height = 792

# Margin configurations
default_margins = {'left': 50, 'right': 50, 'top': 50, 'bottom': 50}
alt_margins = {'left': 72, 'right': 72, 'top': 72, 'bottom': 72}  # 1 inch

grid_spacing = 50
doc = fitz.open()

def draw_margins(page, margins, color=(1, 0, 0)):
    page.draw_line((margins['left'], 0), (margins['left'], page_height), color=color)
    page.draw_line((page_width - margins['right'], 0), (page_width - margins['right'], page_height), color=color)
    page.draw_line((0, margins['top']), (page_width, margins['top']), color=color)
    page.draw_line((0, page_height - margins['bottom']), (page_width, page_height - margins['bottom']), color=color)

def draw_grid(page, margins, spacing, color=(0.7, 0.7, 0.7)):
    for x in range(margins['left'] + spacing, page_width - margins['right'], spacing):
        page.draw_line((x, margins['top']), (x, page_height - margins['bottom']), color=color)
    for y in range(margins['top'] + spacing, page_height - margins['bottom'], spacing):
        page.draw_line((margins['left'], y), (page_width - margins['right'], y), color=color)

def add_header_footer(page, margins, header_text, footer_text):
    page.insert_text((margins['left'], margins['top'] - 40), header_text, fontsize=12, color=(0, 0, 0))
    page.insert_text((margins['left'], page_height - margins['bottom'] + 20), footer_text, fontsize=12, color=(0, 0, 0))

def add_settings_text(page, margins, layout_desc):
    settings_text = f"""Page Size: {page_width} x {page_height} points (Letter Portrait)
Margins:
  Left: {margins['left']} pts
  Right: {margins['right']} pts
  Top: {margins['top']} pts
  Bottom: {margins['bottom']} pts
Layout:
  {layout_desc}"""
    page.insert_text((margins['left'] + 10, margins['top'] + 20), settings_text, fontsize=20, color=(0, 0, 0))

# Page 1
page1 = doc.new_page(width=page_width, height=page_height)
draw_margins(page1, default_margins)
draw_grid(page1, default_margins, grid_spacing)
add_header_footer(page1, default_margins, "Header: Full Layout", "Footer: End of Page 1")
add_settings_text(page1, default_margins, "Margin lines: Red\nGrid lines: Every 50 pts (Gray)\nHeader/Footer: Present")

# Page 2
page2 = doc.new_page(width=page_width, height=page_height)
draw_margins(page2, default_margins)
add_header_footer(page2, default_margins, "Header: Margins Only", "Footer: End of Page 2")
add_settings_text(page2, default_margins, "Margin lines: Red\nGrid lines: None\nHeader/Footer: Present")

# Page 3
page3 = doc.new_page(width=page_width, height=page_height)
draw_grid(page3, {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}, grid_spacing)
add_settings_text(page3, {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}, "Margin lines: None\nGrid lines: Every 50 pts (Gray)\nHeader/Footer: None")

# Page 4
page4 = doc.new_page(width=page_width, height=page_height)
draw_margins(page4, alt_margins)
draw_grid(page4, alt_margins, grid_spacing)
add_header_footer(page4, alt_margins, "Header: Full Layout (Alt Margins)", "Footer: End of Page 4")
add_settings_text(page4, alt_margins, "Margin lines: Red\nGrid lines: Every 50 pts (Gray)\nHeader/Footer: Present\nMargins: 1 inch")

# Page 5
page5 = doc.new_page(width=page_width, height=page_height)
draw_margins(page5, default_margins)
draw_grid(page5, default_margins, grid_spacing)
add_header_footer(page5, default_margins, "Header: Full Layout", "Footer: End of Page 5")
add_settings_text(page5, default_margins, "Margin lines: Red\nGrid lines: Every 50 pts (Gray)\nHeader/Footer: Present")

# Page 6
page6 = doc.new_page(width=page_width, height=page_height)
draw_margins(page6, default_margins)
add_header_footer(page6, default_margins, "Header: Margins Only", "Footer: End of Page 6")
add_settings_text(page6, default_margins, "Margin lines: Red\nGrid lines: None\nHeader/Footer: Present")

# Page 7
page7 = doc.new_page(width=page_width, height=page_height)
draw_grid(page7, {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}, grid_spacing)
add_settings_text(page7, {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}, "Margin lines: None\nGrid lines: Every 50 pts (Gray)\nHeader/Footer: None")

# Page 8
page8 = doc.new_page(width=page_width, height=page_height)
draw_margins(page8, alt_margins)
draw_grid(page8, alt_margins, grid_spacing)
add_header_footer(page8, alt_margins, "Header: Full Layout (Alt Margins)", "Footer: End of Page 8")
add_settings_text(page8, alt_margins, "Margin lines: Red\nGrid lines: Every 50 pts (Gray)\nHeader/Footer: Present\nMargins: 1 inch")
# Save
doc.save("example.pdf")
doc.close()
