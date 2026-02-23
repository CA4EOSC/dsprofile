import pathlib

from dsprofile.lib import (
    reader_type_map,
    Reader
)

class ShapefileReader(Reader):

    format = "shape"

    def __init__(self, filename):
        super().__init__()

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
        pass
