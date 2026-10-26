"""Mint-tin zine: a zine sized to fit an Altoids-style tin. Geometry not defined yet."""

DESCRIPTION = (
    "[not implemented] zine sized to fit a standard or mini Altoids tin; "
    "dimensions still to be researched."
)


def add_arguments(parser):
    parser.add_argument("--tin", choices=["standard", "mini"], default="standard",
                        help="tin size to target (planned)")


def build(src, output, opts):
    raise NotImplementedError("minttin layout geometry has not been defined yet.")
