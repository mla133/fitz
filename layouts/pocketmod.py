"""PocketMod: 8 pages on one side of a sheet, cut in the middle and folded."""
import pymupdf

from .common import PAGE_SIZES, cut_line, place

DESCRIPTION = "8-page PocketMod on a single sheet (extra input pages are ignored)."

# (page_index, rotation) in row-major cell order
LAYOUT_ORDER = [
    (5, 270), (4, 90),
    (6, 270), (3, 90),
    (7, 270), (2, 90),
    (0, 270), (1, 90),
]


def add_arguments(parser):
    pass


def build(src, output, opts):
    page_width, page_height = PAGE_SIZES[opts.page_size]
    mini_width, mini_height = page_width / 2, page_height / 4

    doc = pymupdf.open()
    page = doc.new_page(width=page_width, height=page_height)

    for i, (page_index, rotation) in enumerate(LAYOUT_ORDER):
        x0 = (i % 2) * mini_width
        y0 = (i // 2) * mini_height
        rect = pymupdf.Rect(x0, y0, x0 + mini_width, y0 + mini_height)
        place(page, rect, src, page_index, rotation, label_size=80, guides=opts.guides)

    if opts.guides:
        cut_x = page_width / 2
        cut_line(page, pymupdf.Rect(cut_x, mini_height, cut_x + 0.5, 3 * mini_height))

    doc.save(output)
    doc.close()
