"""Layout registry: name -> module (DESCRIPTION, add_arguments(parser), build(src, out, opts))."""
from . import businesscard, minttin, pocketfold, pocketmod, zine

LAYOUTS = {
    "pocketmod": pocketmod,
    "pocketfold": pocketfold,
    "zine": zine,
    "businesscard": businesscard,
    "minttin": minttin,
}
