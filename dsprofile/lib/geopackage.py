import pathlib
import sys
import warnings

import geopandas as gpd

from io import BytesIO

from dsprofile.lib.reader import Reader


class GeoPackageReader(Reader):

    format = "geopackage"

    def __init__(self, filename):
        """
          GeoPandas closes input file automatically
          and no weakref.finalize is required.
        """
        self.filename = filename
        """
          Suppress warnings due to "non conformant" filename
          when reading input from a buffer
        """
        if isinstance(filename, BytesIO):
            warnings.filterwarnings(module="pyogrio", action="ignore",
                                    category=RuntimeWarning,
                                    message=".*non conformant.*")
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
        """
          Describes the variables of each layer defined in the
          GeoPackage.
          The "geometry" key records the name of the dataframe column
          containing geometrical constructs, or "None" if this is absent.
        """
        layers = []
        for idx, layer in self.layers.iterrows():
            df = gpd.read_file(self.filename, layer=layer["name"])
            layers.append({
                "name": layer["name"],
                "geometry": str(df.active_geometry_name) if hasattr(df, "active_geometry_name") else "None",
                "variables": {col_name: str(df[col_name].dtype) for col_name in df.columns}
            })

        return layers

    def process(self):
        return {"layers": self.read_layers()}
