"""One-sheet, double-sided 8-page zine imposition on a landscape sheet."""
import pymupdf

from .common import PAGE_SIZES, place

DESCRIPTION = (
    "8-page one-sheet zine imposed on 2 landscape sides. Print double-sided, flip on the "
    "short edge, fold the top half down behind the bottom, then fold in half."
)

# 0-based page indexes: (top_left, top_right, bottom_left, bottom_right)
SIDES = [
    (4, 3, 7, 0),
    (2, 5, 1, 6),
]


def add_arguments(parser):
    pass


def build(src, output, opts):
    if src is not None and src.page_count != 8:
        raise ValueError(f"zine needs exactly 8 input pages, got {src.page_count}.")

    short, long_ = PAGE_SIZES[opts.page_size]
    sheet_width, sheet_height = long_, short
    hw, hh = sheet_width / 2, sheet_height / 2

    cells = [
        (pymupdf.Rect(0, 0, hw, hh), 180),
        (pymupdf.Rect(hw, 0, sheet_width, hh), 180),
        (pymupdf.Rect(0, hh, hw, sheet_height), 0),
        (pymupdf.Rect(hw, hh, sheet_width, sheet_height), 0),
    ]

    doc = pymupdf.open()
    for indexes in SIDES:
        # Fully populate each sheet before creating the next; new_page() invalidates earlier pages.
        sheet = doc.new_page(width=sheet_width, height=sheet_height)
        for (rect, rotation), page_index in zip(cells, indexes):
            place(sheet, rect, src, page_index, rotation, label_size=48, guides=False)
    doc.save(output)
    doc.close()
