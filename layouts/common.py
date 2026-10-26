"""Shared helpers for the fitz_convert layouts."""
import pymupdf

PAGE_SIZES = {
    "letter": (612, 792),
    "a4": (595, 842),
}


def load_pages(paths):
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


def place(page, rect, src, page_index, rotation=0, label_size=36, color=(1, 0, 0), guides=True):
    """Draw source page `page_index` into `rect`, or a numbered placeholder if there's no such page."""
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


def cut_line(page, rect, color=(1, 0, 0), thickness=0.5):
    page.draw_rect(rect, color=color, width=thickness)
