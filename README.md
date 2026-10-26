# fitz – PDF mini-book and zine tools

[PyMuPDF](https://pymupdf.readthedocs.io/) tools that turn PDFs and images into
printable folded layouts: PocketMod, PocketFold, a one-sheet zine and
business-card sheets. Everything goes through one command, `fitz_convert.py`.
Output is **US Letter** (612 × 792 pt) unless you pass `--page-size a4`.

## Setup

```powershell
pip install -r requirements.txt     # just PyMuPDF
pip install -e .                    # optional: installs the `fitz-convert` command
```

Requires Python 3.9+. Licensed under the [MIT License](LICENSE).

## Usage

```powershell
python fitz_convert.py <layout> -i IN [IN ...] -o OUT.pdf [options]
python fitz_convert.py -h              # list layouts
python fitz_convert.py <layout> -h     # options for one layout
```

After `pip install -e .` you can use `fitz-convert` in place of `python fitz_convert.py`.

`-i` takes one or more PDFs or images (PNG, JPG, ...). They are concatenated in
order into one page sequence, and one output PDF is written per run.

### Layouts

| Layout | Input pages | Output |
| --- | --- | --- |
| `pocketmod` | first 8 used | 1 Letter sheet: 8 pages, 2 × 4 grid, red cut line |
| `pocketfold` | 10 | Sheet 1: 8 mini-pages and a green cut line. Sheet 2: pages 9 and 10 as two half-pages |
| `zine` | exactly 8 | 2 landscape sides, one-sheet zine (print double-sided, flip on short edge; fold the top half down behind the bottom, then in half) |
| `businesscard` | first page or image | Card sheet (default 3.5 × 2 in, 10 per Letter page) tiled with the input |
| `minttin` | n/a | **Not implemented yet.** Planned: a zine that fits a standard or mini Altoids tin (`--tin standard\|mini`) |

Missing pages in `pocketmod` and `pocketfold` are filled with numbered
placeholders. `zine` fails with an error unless the input has exactly 8 pages.

### Options

| Option | Meaning |
| --- | --- |
| `-i, --input FILE...` | Input PDFs/images (required unless `--placeholder`) |
| `-o, --output PDF` | Output path (required; existing files are overwritten) |
| `--page-size letter\|a4` | Sheet size (default `letter`) |
| `--no-guides` | Omit cell borders and cut lines |
| `--placeholder` | Ignore input; draw numbered pages (or a sample card) |
| `--card-size WxH` | `businesscard` only: card size in inches (default `3.5x2`) |

### Examples

```powershell
python fitz_convert.py pocketmod -i fontsizes.pdf -o pocketmod_output.pdf
python fitz_convert.py pocketfold -i intro.pdf body.pdf -o pocketfold_output.pdf
python fitz_convert.py zine -i zine_with_content.pdf -o zine_imposed_for_print.pdf
python fitz_convert.py businesscard -i card.png -o cards.pdf --card-size 3.5x2
python fitz_convert.py pocketmod --placeholder -o test_layout.pdf
```

**Print:** 100% / "Actual size" (no fit-to-page scaling).

### Project layout

- `fitz_convert.py`: command-line entry point (argparse subcommands).
- `layouts/`: one module per layout plus `common.py`. To add a layout, create a
  module with `DESCRIPTION`, `add_arguments(parser)` and `build(src, output, opts)`,
  then register it in `layouts/__init__.py`.
- `tests/`: pytest suite (`pip install -r requirements-dev.txt`, then `pytest`; lint with `ruff check .`).
- `examples/`: standalone scripts that generate sample content (see below).
- `tools/`: small PDF search utilities (`search_dirs.py`, `extract_search.py`).
- `assets/`: sample images.

The original single-purpose converters (`pocketmod_convert.py`, `pocketfold_convert.py`,
`zine_imposed.py`, `bus_card.py`) were removed; they're in git history before the
`obsolete/` cleanup commit if you need them.

## Making source PDFs

These scripts live in `examples/` and generate content you can feed to the converter.
They read and write the **current working directory**, so `cd` into their folder first.

- **PocketFold sample (10 pages):** `cd examples\pocketfold; python generator.py` writes `generated_document.pdf`.
- **PocketMod sample (8 pages):** `cd examples\pocketmod; python fontsizes.py` writes `fontsizes.pdf`.
  `ebook_layout.py` writes `ebook_layout.pdf`.
- **Zine pages:** `cd examples\zine; python basic.py` writes blank `basic_zine.pdf` (half-letter
  pages, 5.5 × 8.5 in). Edit the call at the bottom of `added_content.py` (page number, title,
  body text, optional image) and run it to produce `zine_with_content.pdf`.
- `examples\zine_layout.py` is a simpler 4-page zine on one Letter page using `assets\map7.png`.

## Other example scripts (`examples/`)

| Script | Output / purpose |
| --- | --- |
| `generator.py` | Sample multi-page PDF with headers, d100 and card-draw grids |
| `dice_roll.py` | `dice_roller_results.pdf` |
| `settings.py`, `settings2.py`, `margins.py` | Margin/grid layout experiments |
| `calendar_added.py`, `content_layout.py` | Multi-page layouts with header/footer guides |
| `paragraph.py`, `func_paragraphs.py` | Paragraph wrapping examples |
| `ebook_a5.py` | A5 eBook page layout |
| `fitz_example.py` | PyMuPDF reference and mint-tin template (95 × 60 mm) |

These are standalone and run directly with `python`; hardcoded output names
will overwrite existing files. Not every output is Letter: `zine/basic.py` is
half-letter, `ebook_a5.py` is A5, and `fitz_example.py` builds a mint-tin label
by design.
