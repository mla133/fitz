"""Business cards: tile the first input page/image N-up on a sheet."""
import pymupdf

from .common import PAGE_SIZES

DESCRIPTION = "Tile the first input page or image as business cards (--placeholder for a template)."


def _card_size(text):
    """Parse 'WxH' inches into (width, height) points."""
    try:
        w, h = (float(v) for v in text.lower().split("x"))
        if w <= 0 or h <= 0:
            raise ValueError
    except ValueError:
        raise ValueError(f"--card-size must look like 3.5x2 (inches), got '{text}'.") from None
    return w * 72, h * 72


def add_arguments(parser):
    parser.add_argument("--card-size", default="3.5x2", metavar="WxH",
                        help="card size in inches (default: 3.5x2)")


def build(src, output, opts):
    """Write a sheet of cards tiled with page 1 of `src` (or a template if None) to `output`."""
    page_width, page_height = PAGE_SIZES[opts.page_size]
    card_w, card_h = _card_size(opts.card_size)
    cols, rows = int(page_width // card_w), int(page_height // card_h)
    if cols < 1 or rows < 1:
        raise ValueError("card size doesn't fit on the page.")

    # Center the grid so the margins are even.
    x_off = (page_width - cols * card_w) / 2
    y_off = (page_height - rows * card_h) / 2

    doc = pymupdf.open()
    page = doc.new_page(width=page_width, height=page_height)

    for i in range(cols * rows):
        x0 = x_off + (i % cols) * card_w
        y0 = y_off + (i // cols) * card_h
        rect = pymupdf.Rect(x0, y0, x0 + card_w, y0 + card_h)

        if src is not None:
            page.show_pdf_page(rect, src, 0)
        else:
            page.insert_textbox(pymupdf.Rect(x0, y0 + card_h / 3, x0 + card_w, y0 + card_h),
                                "John Doe\nDeveloper", fontsize=12, align=1)
            logo = pymupdf.Rect(x0 + 10, y0 + 10, x0 + 50, y0 + 50)
            page.draw_rect(logo, color=(0.5, 0.5, 0.5), fill=(0.8, 0.8, 0.8))
            page.insert_textbox(logo, "Logo", fontsize=8, align=1)

        if opts.guides:
            page.draw_rect(rect, color=(0, 0, 1), width=1)

    doc.save(output)
    doc.close()
