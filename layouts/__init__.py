"""Layout registry: name -> module exposing DESCRIPTION, add_arguments(parser), build(src, output, opts)."""
from . import businesscard, minttin, pocketfold, pocketmod, zine

LAYOUTS = {
    "pocketmod": pocketmod,
    "pocketfold": pocketfold,
    "zine": zine,
    "businesscard": businesscard,
    "minttin": minttin,
}
