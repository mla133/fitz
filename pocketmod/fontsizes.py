import fitz  # PyMuPDF

# Page dimensions
page_width = 612
page_height = 792

# Margin configurations
default_margins = {'left': 50, 'right': 50, 'top': 50, 'bottom': 50}
alt_margins = {'left': 72, 'right': 72, 'top': 72, 'bottom': 72}  # 1 inch

# Grid spacing
grid_spacing = 50

# Font sizes for each page
font_sizes = [16, 18, 20, 24, 28, 32, 36, 40]

# Lorem Ipsum text
lorem_text = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
)

# Create a new PDF document
doc = fitz.open()

# Function to draw margins
def draw_margins(page, margins, color=(1, 0, 0)):
    page.draw_line((margins['left'], 0), (margins['left'], page_height), color=color)
    page.draw_line((page_width - margins['right'], 0), (page_width - margins['right'], page_height), color=color)
    page.draw_line((0, margins['top']), (page_width, margins['top']), color=color)
    page.draw_line((0, page_height - margins['bottom']), (page_width, page_height - margins['bottom']), color=color)

# Function to draw grid
def draw_grid(page, margins, spacing, color=(0.7, 0.7, 0.7)):
    for x in range(margins['left'] + spacing, page_width - margins['right'], spacing):
        page.draw_line((x, margins['top']), (x, page_height - margins['bottom']), color=color)
    for y in range(margins['top'] + spacing, page_height - margins['bottom'], spacing):
        page.draw_line((margins['left'], y), (page_width - margins['right'], y), color=color)

# Function to add font size label
def add_font_size_label(page, margins, font_size):
    label_text = f"Font Size: {font_size} pt"
    page.insert_text((margins['left'], margins['top'] - 30), label_text, fontsize=10, color=(0, 0, 1))

# Function to add lorem text
def add_lorem_text(page, margins, font_size):
    rect = fitz.Rect(margins['left'], margins['top'], page_width - margins['right'], page_height - margins['bottom'])
    page.insert_textbox(rect, lorem_text, fontsize=font_size, color=(0, 0, 0), align=0)

# Generate 8 pages with varying font sizes
for i in range(8):
    page = doc.new_page(width=page_width, height=page_height)
    font_size = font_sizes[i]
    margins = default_margins if i % 2 == 0 else alt_margins
    draw_margins(page, margins)
    draw_grid(page, margins, grid_spacing)
    add_font_size_label(page, margins, font_size)
    add_lorem_text(page, margins, font_size)

# Save the updated PDF
doc.save("fontsizes.pdf")
doc.close()
