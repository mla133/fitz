# fitz – PDF mini-book and zine generators

Small [PyMuPDF](https://pymupdf.readthedocs.io/) scripts that build printable
PDFs: PocketFold, PocketMod, business-card sheets, and an 8-page zine. All
output is **US Letter** (612 × 792 pt) unless noted.

## Setup

```powershell
pip install pymupdf
```

Every script is run directly with `python` and reads/writes files in the
**current working directory**, so `cd` into the script's folder first.

## Unified converter (`fitz_convert.py`)

```powershell
python fitz_convert.py <layout> -i IN [IN ...] -o OUT.pdf [options]
```

Layouts: `pocketmod`, `pocketfold`, `zine`, `businesscard`, `minttin` (stub, not implemented yet; planned to fit standard and mini Altoids tins).
`-i` takes one or more PDFs/images, concatenated in order. Options: `--page-size letter|a4`,
`--no-guides` (omit borders/cut lines), `--placeholder` (no input; numbered or template cells),
`--card-size WxH` (businesscard, inches). `zine` needs exactly 8 pages, `pocketfold` 10,
`pocketmod` uses the first 8; `businesscard` tiles the first page or image.

```powershell
python fitz_convert.py pocketmod -i fontsizes.pdf -o pocketmod_output.pdf
python fitz_convert.py businesscard -i card.png -o cards.pdf
python fitz_convert.py -h
```

The original per-layout converters are archived in `obsolete/`; the sections below
describe the source-PDF generators and the old workflow, so substitute `fitz_convert.py` for the `*_convert.py` / `bus_card.py` / `zine_imposed.py` steps.

## PocketFold (`pocketfold/`)

An 8-page mini-book on one side of a Letter sheet, plus two half-page
sheets on the back (10 pages total).

1. Generate a 10-page source PDF (sample content, written to `generated_document.pdf`):
   ```powershell
   cd pocketfold
   python generator.py
   ```
2. Impose it into the PocketFold layout:
   ```powershell
   python pocketfold_convert.py
   ```
   Output: `pocketfold_output.pdf`.

To use your own content, replace `generated_document.pdf` with your own PDF
(10 pages) or edit the `input_pdf_path` in the last line of
`pocketfold_convert.py`. Uncomment `create_pocketfold_pdf()` instead to get a
numbered dummy layout without any input.

Page 1 holds 8 mini-pages (2 × 4 grid, alternating rotation); a green line
marks the cut. Page 2 holds pages 9 and 10 as two rotated half-pages.

## PocketMod (`pocketmod/`)

An 8-page booklet from a single Letter sheet: print one side, fold, cut the
center slit, and fold into a booklet.

1. Create a source PDF (text sample with various font sizes → `fontsizes.pdf`):
   ```powershell
   cd pocketmod
   python fontsizes.py
   ```
   Alternatively use `ebook_layout.py` (writes `ebook_layout.pdf`; point
   `example_pdf` at it).
2. Impose it:
   ```powershell
   python pocketmod_convert.py
   ```
   Output: `pocketmod_output.pdf`.

The input PDF is set by `example_pdf` at the top of `pocketmod_convert.py`;
only the first 8 pages are used. Uncomment `create_pocketmod_pdf()` at the
bottom for a numbered dummy layout. The red line marks the cut.

**Print:** Letter, 100% / "Actual size" (no fit-to-page scaling).

## Business cards (`business_card/`)

```powershell
cd business_card
python bus_card.py
```

Output: `business_cards_with_borders.pdf` – a Letter sheet filled with
3.5 × 2 in cards (2 × 5 = 10 cards) with blue borders, placeholder name text,
and a gray "Logo" box. To customize, edit `placeholder_text`, the logo
dimensions, and card size constants in `create_business_card_layout_with_visible_borders`.

## Zine (`zine/`)

An 8-page, single-sheet folded zine (half-letter pages, 5.5 × 8.5 in).

1. Create the blank pages (`basic_zine.pdf`):
   ```powershell
   cd zine
   python basic.py
   ```
2. Add content to a page (`zine_with_content.pdf`). Edit the call at the
   bottom of `added_content.py` to set the page number, title, body text,
   and optional image path (e.g. `add_content_to_page(doc, 0, "Title", "Text", "my_image.png")`):
   ```powershell
   python added_content.py
   ```
3. Impose for printing on a landscape Letter sheet (`zine_imposed_for_print.pdf`):
   ```powershell
   python zine_imposed.py
   ```
   The input must have exactly 8 pages. Print **double-sided, flip on short
   edge**. Fold the top half down behind the bottom, then fold in half so
   Page 1 is the front cover.

`zine_layout.py` (repo root) is a simpler 4-page zine on one Letter page:
call `create_zine(image_paths, text_content, output_file)` from your own code.

## Other scripts (repo root)

| Script | Output / purpose |
| --- | --- |
| `generator.py` | Sample multi-page PDF with headers, d100 and card-draw grids |
| `dice-roll.py` | `dice_roller_results.pdf` |
| `settings.py`, `settings2.py`, `margins.py` | Margin/grid layout experiments |
| `calendar_added.py`, `content_layout.py` | Multi-page layouts with header/footer guides |
| `paragraph.py`, `func_paragraphs.py` | Paragraph wrapping examples |
| `layout.py`, `layout2.py`, `layout3.py` | eBook page layouts (`layout.py` is A5) |
| `fitz_example.py` | PyMuPDF reference and mint-tin template (95 × 60 mm) |

## Notes

- Scripts with hardcoded input/output names will overwrite existing files.
- Not every output is Letter: `zine/basic.py` is half-letter, `layout.py`
  is A5, and `fitz_example.py` builds a mint-tin label by design.
