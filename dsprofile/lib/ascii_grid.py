import pathlib
import sys

from dsprofile.lib.reader import Reader
from dsprofile.utils import logged


class ASCIIGRIDReader(Reader):
    """
      A Reader type for ESRI ASCII Grid datasets.
    """

    format = "ascii_grid"

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.dataset = self.read_dataset(filename)

    @classmethod
    def build_subparser(cls, sp):
        parser = sp.add_parser(cls.format,
                               help="Extracts metadata from ESRI ASCII Grid files")
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

    @staticmethod
    def _parse_value(key, value):
        if key in ("ncols", "nrows"):
            return int(value)
        return float(value)

    @classmethod
    def read_dataset(cls, filename):
        header_keys = {
            "ncols",
            "nrows",
            "xllcorner",
            "xllcenter",
            "yllcorner",
            "yllcenter",
            "cellsize",
            "nodata_value"
        }

        header = {}
        data_rows = 0

        try:
            with open(filename, "r", encoding="utf-8") as handle:
                for line in handle:
                    stripped = line.strip()
                    if not stripped:
                        continue

                    parts = stripped.split(None, 1)
                    if len(parts) == 2 and parts[0].lower() in header_keys:
                        key = parts[0].lower()
                        try:
                            header[key] = cls._parse_value(key, parts[1])
                        except ValueError as e:
                            print(f"Invalid header value for '{key}' in '{filename}': {e}",
                                  file=sys.stderr)
                            sys.exit(1)
                        continue

                    data_rows += 1
        except (OSError, PermissionError, FileNotFoundError) as e:
            print(f"Unable to read dataset '{filename}': {e}", file=sys.stderr)
            sys.exit(1)

        required = {"ncols", "nrows", "cellsize"}
        if not required.issubset(header):
            missing = sorted(required.difference(header.keys()))
            print(f"Missing ASCII Grid header fields in '{filename}': {','.join(missing)}",
                  file=sys.stderr)
            sys.exit(1)

        if not ({"xllcorner", "xllcenter"} & set(header.keys())):
            print(f"Missing x-origin in ASCII Grid header for '{filename}'",
                  file=sys.stderr)
            sys.exit(1)

        if not ({"yllcorner", "yllcenter"} & set(header.keys())):
            print(f"Missing y-origin in ASCII Grid header for '{filename}'",
                  file=sys.stderr)
            sys.exit(1)

        path = pathlib.Path(filename)
        return {
            "header": header,
            "data": {
                "row_count": data_rows,
                "expected_row_count": int(header["nrows"])
            },
            "companion_files": {
                "prj": path.with_suffix(".prj").exists(),
                "tfw": path.with_suffix(".tfw").exists()
            }
        }

    @logged
    def process(self):
        return self.dataset