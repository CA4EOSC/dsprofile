import pathlib
import sys
import warnings

import geopandas as gpd

from contextlib import nullcontext
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

        with warnings.catch_warnings() if isinstance(filename, BytesIO) else nullcontext():
            #  It's necessary to repeat this check here as
            #  possible nullcontext results in permanent
            #  change to global warnings
            if isinstance(filename, BytesIO):
                warnings.filterwarnings(module="pyogrio", action="ignore",
                                        category=RuntimeWarning,
                                        message=".*non conformant.*")
            try:
                self.layers = gpd.list_layers(filename)
            # RuntimeError captures pyogrio.error's general `DataSourceError`
            except (OSError, PermissionError, FileNotFoundError, RuntimeError) as e:
                print(f"{e} for file '{filename}'", file=sys.stderr)
                sys.exit(1)

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
            try:
                with warnings.catch_warnings() if isinstance(self.filename, BytesIO) else nullcontext():
                    if isinstance(self.filename, BytesIO):
                        warnings.filterwarnings(module="pyogrio", action="ignore",
                                                category=RuntimeWarning,
                                                message=".*non conformant.*")
                    df = gpd.read_file(self.filename, layer=layer["name"])
            except (OSError, PermissionError, FileNotFoundError, RuntimeError) as e:
                print(f"{e} for file '{self.filename}'", file=sys.stderr)
                sys.exit(1)
            layers.append({
                "name": layer["name"],
                "geometry": str(df.active_geometry_name) if hasattr(df, "active_geometry_name") else "None",
                "variables": {col_name: str(df[col_name].dtype) for col_name in df.columns}
            })

        return layers

    def process(self):
        return {"layers": self.read_layers()}
