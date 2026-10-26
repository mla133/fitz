"""Shared helpers for the fitz_convert layouts."""
from __future__ import annotations

from typing import Iterable, Optional, Tuple

import pymupdf

PAGE_SIZES = {
    "letter": (612, 792),
    "a4": (595, 842),
}


def load_pages(paths: Iterable[str]) -> pymupdf.Document:
    """Concatenate PDFs and images into one in-memory PDF (one page per source page/image)."""
    combined = pymupdf.open()
    for path in paths:
        src = pymupdf.open(path)
        if src.is_pdf:
            combined.insert_pdf(src)
        else:
            combined.insert_pdf(pymupdf.open("pdf", src.convert_to_pdf()))
        src.close()
    return combined


def place(
    page: pymupdf.Page,
    rect: pymupdf.Rect,
    src: Optional[pymupdf.Document],
    page_index: int,
    rotation: int = 0,
    label_size: int = 36,
    color: Tuple[float, float, float] = (1, 0, 0),
    guides: bool = True,
) -> None:
    """Draw source page `page_index` into `rect`, or a numbered placeholder if it doesn't exist."""
    if src is not None and 0 <= page_index < src.page_count:
        page.show_pdf_page(rect, src, page_index, rotate=rotation)
    else:
        shape = page.new_shape()
        shape.draw_rect(rect)
        shape.finish(color=color, fill=None)
        shape.commit()
        page.insert_textbox(rect, f"Page {page_index + 1}", fontsize=label_size,
                            rotate=rotation, align=1)
    if guides:
        page.draw_rect(rect, color=(0, 0, 0), width=1)


def cut_line(
    page: pymupdf.Page,
    rect: pymupdf.Rect,
    color: Tuple[float, float, float] = (1, 0, 0),
    thickness: float = 0.5,
) -> None:
    """Draw a thin rectangle used as a cut line."""
    page.draw_rect(rect, color=color, width=thickness)
