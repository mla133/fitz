import pymupdf
import pytest

from fitz_convert import main
from layouts import LAYOUTS, businesscard, pocketfold, pocketmod, zine
from layouts.common import PAGE_SIZES, load_pages


def make_pdf(path, pages):
    doc = pymupdf.open()
    for n in range(1, pages + 1):
        page = doc.new_page(width=300, height=400)
        page.insert_text((50, 100), f"SRC{n}", fontsize=40)
    doc.save(path)
    doc.close()
    return str(path)


def run(layout, out, *args):
    main([layout, "-o", str(out), *args])
    return pymupdf.open(str(out))


def text_of(page):
    return page.get_text()


# --- layout math -----------------------------------------------------------

@pytest.mark.parametrize("module, count", [(pocketmod, 8), (pocketfold, 10), (zine, 8)])
def test_page_orders_cover_every_page_once(module, count):
    orders = {
        pocketmod: [p for p, _ in pocketmod.LAYOUT_ORDER],
        pocketfold: [p for p, _ in pocketfold.FRONT_ORDER + pocketfold.BACK_ORDER],
        zine: [p for side in zine.SIDES for p in side],
    }[module]
    assert sorted(orders) == list(range(count))


@pytest.mark.parametrize("size", sorted(PAGE_SIZES))
def test_pocketmod_cells_tile_the_sheet(tmp_path, size):
    doc = run("pocketmod", tmp_path / "o.pdf", "--placeholder", "--page-size", size)
    width, height = PAGE_SIZES[size]
    page = doc[0]
    assert (page.rect.width, page.rect.height) == (width, height)
    boxes = [d["rect"] for d in page.get_drawings() if d["rect"].width == pytest.approx(width / 2)
             and d["rect"].height == pytest.approx(height / 4)]
    # Each of the 8 cells is drawn twice (placeholder outline + guide border).
    assert len({(round(r.x0), round(r.y0)) for r in boxes}) == 8
    assert sum(r.get_area() for r in {(round(b.x0), round(b.y0)): b for b in boxes}.values()) \
        == pytest.approx(width * height)


def test_zine_sheets_are_landscape(tmp_path):
    doc = run("zine", tmp_path / "o.pdf", "--placeholder")
    assert doc.page_count == 2
    for page in doc:
        assert (page.rect.width, page.rect.height) == (792, 612)


def test_businesscard_grid_fits_and_is_centered():
    cols, rows = int(612 // (3.5 * 72)), int(792 // (2 * 72))
    assert (cols, rows) == (2, 5)
    w, h = businesscard._card_size("3.5x2")
    assert (w, h) == (252, 144)


@pytest.mark.parametrize("bad", ["3.5", "axb", "0x2", "-1x2"])
def test_businesscard_rejects_bad_size(bad):
    with pytest.raises(ValueError):
        businesscard._card_size(bad)


# --- output checks ---------------------------------------------------------

def test_pocketmod_output(tmp_path):
    src = make_pdf(tmp_path / "in.pdf", 8)
    doc = run("pocketmod", tmp_path / "o.pdf", "-i", src)
    assert doc.page_count == 1
    assert (doc[0].rect.width, doc[0].rect.height) == (612, 792)
    text = text_of(doc[0])
    for n in range(1, 9):
        assert f"SRC{n}" in text


def test_pocketmod_fills_missing_pages_with_placeholders(tmp_path):
    src = make_pdf(tmp_path / "in.pdf", 3)
    doc = run("pocketmod", tmp_path / "o.pdf", "-i", src)
    text = " ".join(text_of(doc[0]).split())
    assert "SRC3" in text and "Page 4" in text and "Page 8" in text


def test_pocketfold_output(tmp_path):
    src = make_pdf(tmp_path / "in.pdf", 10)
    doc = run("pocketfold", tmp_path / "o.pdf", "-i", src)
    assert doc.page_count == 2
    assert all("SRC" in text_of(p) for p in doc)
    assert "SRC9" in text_of(doc[1]) and "SRC10" in text_of(doc[1])


def test_zine_output_and_page_count_validation(tmp_path):
    good = make_pdf(tmp_path / "eight.pdf", 8)
    doc = run("zine", tmp_path / "o.pdf", "-i", good)
    assert doc.page_count == 2
    bad = make_pdf(tmp_path / "five.pdf", 5)
    with pytest.raises(SystemExit):
        main(["zine", "-i", bad, "-o", str(tmp_path / "bad.pdf")])


def test_businesscard_output_tiles_cards(tmp_path):
    src = make_pdf(tmp_path / "in.pdf", 1)
    doc = run("businesscard", tmp_path / "o.pdf", "-i", src)
    assert doc.page_count == 1
    assert text_of(doc[0]).count("SRC1") == 10


def test_no_guides_draws_fewer_shapes(tmp_path):
    with_guides = run("pocketmod", tmp_path / "a.pdf", "--placeholder")
    without = run("pocketmod", tmp_path / "b.pdf", "--placeholder", "--no-guides")
    assert len(without[0].get_drawings()) < len(with_guides[0].get_drawings())


def test_images_are_accepted_as_input(tmp_path):
    pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 20, 20), False)
    pix.clear_with(200)
    img = tmp_path / "pic.png"
    pix.save(str(img))
    assert load_pages([str(img)]).page_count == 1
    assert run("businesscard", tmp_path / "o.pdf", "-i", str(img)).page_count == 1


# --- CLI -------------------------------------------------------------------

def test_no_arguments_prints_help(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["fitz_convert.py"])
    assert main() == 0
    out = capsys.readouterr().out
    assert "usage:" in out and "pocketmod" in out and "zine" in out


def test_cli_requires_input_unless_placeholder(tmp_path):
    with pytest.raises(SystemExit):
        main(["pocketmod", "-o", str(tmp_path / "o.pdf")])


def test_cli_reports_unreadable_input(tmp_path):
    with pytest.raises(SystemExit):
        main(["pocketmod", "-i", str(tmp_path / "missing.pdf"), "-o", str(tmp_path / "o.pdf")])


def test_minttin_is_not_implemented(tmp_path):
    with pytest.raises(SystemExit):
        main(["minttin", "--placeholder", "-o", str(tmp_path / "o.pdf")])


def test_every_layout_has_required_interface():
    for module in LAYOUTS.values():
        assert module.DESCRIPTION
        assert callable(module.add_arguments) and callable(module.build)
