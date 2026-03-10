from .reader import (  # noqa: F401
    Reader,
    reader_type_map,
    make_reader
)

from .netcdf import NetCDFReader    # noqa: F401
from .tiff import GeoTIFFReader     # noqa: F401
from .shape import ShapefileReader  # noqa: F401
