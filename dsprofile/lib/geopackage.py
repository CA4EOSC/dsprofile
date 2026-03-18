import pathlib
import sys

import geopandas as gpd

from collections.abc import Sequence

from dsprofile.lib.reader import Reader


class GeoPackageReader(Reader):

    format = "geopackage"

    def __init__(self, filename):
        """
          GeoPandas closes input file automatically
          and no weakref.finalize is required.
        """
        self.filename = filename
        self.layers = gpd.list_layers(filename)

    @classmethod
    def build_subparser(cls, sp):
        parser = sp.add_parser(cls.format,
                               help="Extracts metadata from GeoPackage files")
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

    def read_layers(self):
        layers = {}
        for layer in self.layers["name"]:
            df = gpd.read_file(self.filename, layer=layer)
            layers[layer] = {col_name: str(df[col_name].dtype) for col_name in df.columns}

        return layers

    def process(self):
        return {"layers": self.read_layers()}


if __name__ == "__main__":
    from pprint import pprint
    gpr = GeoPackageReader("/mnt/xfr/bdnb.gpkg")
    layers = gpr.process()
    pprint(layers)
