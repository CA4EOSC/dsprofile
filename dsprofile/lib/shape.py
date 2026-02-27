import pathlib
import sys
import weakref

import fiona
from fiona import Collection

from dsprofile.lib import Reader


class ShapefileReader(Reader):

    format = "shape"

    def __init__(self, filename):
        super().__init__()
        self.shp = self.__class__.read_dataset(filename)
        self._finalizer = weakref.finalize(self, self.finalize_close, self.shp)

    @staticmethod
    def finalize_close(shpinst):
        if not isinstance(shpinst, Collection):
            return

        if not shpinst.closed:
            shpinst.close()

    def close(self):
        if self._finalizer.alive:
            self._finalizer()

    @classmethod
    def build_subparser(cls, sp):
        parser = sp.add_parser(cls.format,
                               help="Extracts metadata from ESRI Shape files")
        parser.add_argument("filename", type=pathlib.Path)
        parser.add_argument("-m", "--omit-metadata", action="store_true",
                            help="Output only Shape file contents, not file metadata")
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
            "bounds": self.shp.bounds,
            "features": []
        }

        units, factor = self.shp.crs.units_factor
        output["units"] = units
        output["factor"] = factor

        auth = self.shp.crs.to_authority()
        if auth is not None:
            if len(auth) == 2:
                registry, code = auth
                output["crs"] = f"{registry}:{code}"
            elif len(auth) == 1:
                output["crs"] = str(auth)

        for feat in self.shp:
            fdata = {
                "type": feat.geometry.type,
                "coordinates": len(feat.geometry.coordinates[0]),
                "properties": {k: v for k, v in feat.properties.items()}
            }
            output["features"].append(fdata)

        return output

    @staticmethod
    def read_dataset(filename):
        try:
            shp = fiona.open(filename)
        except fiona.errors.DriverError as e:
            print(f"Unable to read '{filename}': {e}", file=sys.stderr)
            sys.exit(1)

        return shp
