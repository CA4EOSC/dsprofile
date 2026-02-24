import pathlib
import sys
import weakref

from dsprofile.lib import Reader

import rasterio as rio


class GeoTIFFReader(Reader):

    format = "tiff"

    def __init__(self, filename):
        super().__init__()
        self.tif = rio.open(filename, 'r')
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
        parser.add_argument("-m", "--omit-metadata", action="store_true",
                            help="Output only GeoTIFF file contents, not file metadata")
        parser.add_argument("-d", "--omit-digest", action="store_true",
                            help="Do not include a hash digest in file metadata")
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
            "units": self.tif.units
        }
        auth = self.tif.crs.to_authority()
        if auth is not None:
            if len(auth) == 2:
                registry, code = auth
                output["proj"] = f"{registry}:{code}"
            elif len(auth) == 1:
                output["proj"] = str(auth)

        return output


if __name__ == "__main__":
    f = "/home/paul/caeosc/data/california/neon-sjer-site/2013/lidar/SJER_lidarDSM.tif"
    r = GeoTIFFReader(f)
    p = r.process()
    breakpoint()
