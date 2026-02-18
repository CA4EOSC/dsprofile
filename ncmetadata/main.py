import argparse
import json
import pathlib
import sys

from ncmetadata.reader import process_file
from ncmetadata.util import make_file_profile


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="ncmetadata",
        description="Extracts metadata from netCDF4 files",
        epilog="TODO: attribution/repo/docs"
    )

    parser.add_argument("filename", type=pathlib.Path)
    parser.add_argument("-o", "--order-by", choices=["category", "group"],
                        default="group", help="(default group)")
    parser.add_argument("-e", "--exclude-groups", metavar="<group0>,<group1>,...",
                        help="Exclude each of the named <group> arguments")
    parser.add_argument("-m", "--omit-metadata", action="store_true",
                        help="Output only netCDF file contents, not file metadata")
    parser.add_argument("-d", "--omit-digest", action="store_true",
                        help="Do not include a hash digest in file metadata")

    return parser.parse_args()


def handle_args(args):
    if args.filename.is_dir():
        print(f"A valid file is required not directory '{args.filename}'",
              file=sys.stderr)
        sys.exit(1)

    output = {}
    if not args.omit_metadata:
        output["metadata"] = make_file_profile(args)

    exclude = args.exclude_groups.split(',') if args.exclude_groups else []
    output["content"] = process_file(args.filename, args.order_by, exclude)

    print(json.dumps(output, indent=2))


def main():
    args = parse_args(sys.argv)
    handle_args(args)
    sys.exit(0)


if __name__ == "__main__":
    main()
