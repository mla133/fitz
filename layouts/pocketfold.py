"""PocketFold: 8 mini-pages on one sheet plus 2 half-pages on the back (10 pages)."""
import pymupdf

from .common import PAGE_SIZES, cut_line, place

DESCRIPTION = "10-page PocketFold: 8 mini-pages on sheet 1, 2 half-pages on sheet 2."

FRONT_ORDER = [
    (3, 270), (1, 90),
    (4, 270), (0, 90),
    (5, 270), (7, 90),
    (6, 270), (2, 90),
]
BACK_ORDER = [(8, 270), (9, 270)]


def add_arguments(parser):
    """No layout-specific options."""


def build(src, output, opts):
    """Write the two-sheet PocketFold for `src` (or placeholders if None) to `output`."""
    page_width, page_height = PAGE_SIZES[opts.page_size]
    mini_width, mini_height = page_width / 2, page_height / 4
    half_height = page_height / 2

    doc = pymupdf.open()

    page1 = doc.new_page(width=page_width, height=page_height)
    for i, (page_index, rotation) in enumerate(FRONT_ORDER):
        x0 = (i % 2) * mini_width
        y0 = (i // 2) * mini_height
        rect = pymupdf.Rect(x0, y0, x0 + mini_width, y0 + mini_height)
        place(page1, rect, src, page_index, rotation, label_size=80, guides=opts.guides)
    if opts.guides:
        cut_line(page1, pymupdf.Rect(0, half_height, page_width / 2, half_height + 0.5),
                 color=(0, 1, 0))

    page2 = doc.new_page(width=page_width, height=page_height)
    for i, (page_index, rotation) in enumerate(BACK_ORDER):
        rect = pymupdf.Rect(0, i * half_height, page_width, (i + 1) * half_height)
        place(page2, rect, src, page_index, rotation, label_size=36, color=(0, 0, 1),
              guides=opts.guides)

    doc.save(output)
    doc.close()
