import argparse
import json
import logging
import sys


from dsprofile.lib import (
    reader_type_map,
    make_reader
)

from dsprofile.config import log_config
from dsprofile.utils import make_file_profile


def parse_args(argv):
    """
      Build an argparse environment for the package and any defined
      Reader subclasses.
      Note that each Reader subtype must implement cls.build_subparser
      to create any type-specific cli arguments it requires.
    """
    parser = argparse.ArgumentParser(
        prog="dsprofile",
        description="Describes datasets in a variety of formats",
        epilog="For more information, see ca4eosc.github.io/dsprofile"
    )

    parser.add_argument("-m", "--omit-metadata",
        action="store_true",
        default=False,
        help="Output only file contents, not file metadata")
    parser.add_argument("-d", "--omit-digest",
        action="store_true",
        default=False,
        help="Do not include a hash digest in file metadata")
    parser.add_argument("-l", "--log-level",
        metavar="<level>",
        default="INFO",
        help="Specify the minimal log level")

    sp = parser.add_subparsers(title="Dataset formats",
                               dest="command")
    # Delegate per-type subparser to each defined sub-type...
    for cls in reader_type_map.values():
        cls.build_subparser(sp)

    if len(argv) == 1:
        parser.print_help()
        parser.exit(0)

    args = parser.parse_args()
    return args


def handle_args(args):
    output = {}

    if not hasattr(args, "filename"):
        print("A filename argument must be provided",
              file=sys.stderr)
        sys.exit(1)

    if hasattr(args, "log_level"):
        if args.log_level not in logging.getLevelNamesMapping():
            print(f"Invalid log level '{args.log_level}': ",
                  f"Must be one of {','.join(logging.getLevelNamesMapping().keys())}",
                file=sys.stderr)
            sys.exit(1)
        log_config(args.log_level)

    if hasattr(args, "omit_metadata") and not args.omit_metadata:
        output["metadata"] = make_file_profile(args)

    inst = make_reader(args)
    output["content"] = inst.process()
    print(json.dumps(output, indent=2))


def main():
    args = parse_args(sys.argv)
    handle_args(args)
    sys.exit(0)


if __name__ == "__main__":
    main()
