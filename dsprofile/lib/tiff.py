import pathlib
import sys
import weakref

from dsprofile.lib.reader import Reader

import rasterio as rio
from rasterio.errors import RasterioIOError


class GeoTIFFReader(Reader):
    """
      A Reader instance to process GeoTiff format data.
    """

    format = "geotiff"

    def __init__(self, filename):
        super().__init__()
        try:
            self.tif = rio.open(filename, 'r')
        except RasterioIOError as e:
            print(f"Unable to read dataset '{filename}': {e}", file=sys.stderr)
            sys.exit(1)

        self._finalizer = weakref.finalize(self, self.finalize_close, self.tif)

    @staticmethod
    def finalize_close(rioinst):
        if not isinstance(rioinst, rio.io.DatasetReader):
            return

        if not rioinst.closed:
            rioinst.close()

    def close(self):
        if self._finalizer.alive:
            self._finalizer()

    @classmethod
    def build_subparser(cls, sp):
        parser = sp.add_parser(cls.format,
                               help="Extracts metadata from GeoTIFF files")
        parser.add_argument("filename", type=pathlib.Path)

        return parser

    @classmethod
    def handle_args(cls, args):
        if args.filename.is_dir():
            print(f"A valid file is required not directory '{args.filename}'",
                  file=sys.stderr)
            sys.exit(1)

        ctor_args = [args.filename]
        ctor_kwargs = {}

        return ctor_args, ctor_kwargs

    def process(self):
        output = {
            "shape": {
                "width": self.tif.width,
                "height": self.tif.height
            },
            "bands": {idx: dtype for idx, dtype in zip(self.tif.indexes, self.tif.dtypes)},
            "bounds": {
                "left": self.tif.bounds.left,
                "bottom": self.tif.bounds.bottom,
                "right": self.tif.bounds.right,
                "top": self.tif.bounds.top
            },
            "units": self.tif.crs.linear_units,
            "lin_step": self.tif.res
        }
        auth = self.tif.crs.to_authority()
        if auth is not None:
            if len(auth) == 2:
                registry, code = auth
                output["crs"] = f"{registry}:{code}"
            elif len(auth) == 1:
                output["crs"] = str(auth)

        return output
