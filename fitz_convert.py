"""Convert PDFs/images into printable folded-booklet and card layouts.

    python fitz_convert.py pocketmod -i book.pdf -o out.pdf
    python fitz_convert.py zine -i a.pdf b.png -o zine.pdf
    python fitz_convert.py businesscard --placeholder -o cards.pdf
"""
import argparse
import sys

from layouts import LAYOUTS
from layouts.common import PAGE_SIZES, load_pages


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="layout", required=True, metavar="LAYOUT")
    for name, module in LAYOUTS.items():
        p = sub.add_parser(name, help=module.DESCRIPTION, description=module.DESCRIPTION)
        p.add_argument("-i", "--input", nargs="+", metavar="FILE",
                       help="input PDFs/images, concatenated in order")
        p.add_argument("-o", "--output", required=True, metavar="PDF", help="output PDF path")
        p.add_argument("--page-size", choices=sorted(PAGE_SIZES), default="letter")
        p.add_argument("--no-guides", dest="guides", action="store_false",
                       help="omit cell borders and cut lines")
        p.add_argument("--placeholder", action="store_true",
                       help="ignore input and draw numbered/template placeholders")
        module.add_arguments(p)
    return parser


def main(argv=None):
    parser = build_parser()
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        parser.print_help()
        return 0
    opts = parser.parse_args(argv)

    if opts.placeholder:
        src = None
    elif not opts.input:
        parser.error("-i/--input is required unless --placeholder is given")
    else:
        try:
            src = load_pages(opts.input)
        except Exception as exc:
            parser.error(f"could not read input: {exc}")

    try:
        LAYOUTS[opts.layout].build(src, opts.output, opts)
    except (ValueError, NotImplementedError) as exc:
        parser.error(str(exc))
    finally:
        if src is not None:
            src.close()
    print(f"Wrote {opts.output}")


if __name__ == "__main__":
    sys.exit(main())
