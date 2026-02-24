import argparse
import json
import sys


from dsprofile.lib import (
    reader_type_map,
    make_reader
)

from dsprofile.util import make_file_profile


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="dsprofile",
        description="Describes datasets in a variety of formats",
        epilog="TODO: attribution/repo/docs"
    )

    sp = parser.add_subparsers(title="Dataset formats",
                               dest="command")
    for cls in reader_type_map.values():
        cls.build_subparser(sp)

    if len(argv) == 1:
        parser.print_help()
        parser.exit(0)

    args = parser.parse_args()
    return args


def handle_args(args):
    output = {}
    if hasattr(args, "omit_metadata") and not args.omit_metadata:
        output["metadata"] = make_file_profile(args)

    inst = make_reader(args)
    #output["content"] = process_file(args.filename, args.order_by, exclude)
    output["content"] = inst.process()
    print(json.dumps(output, indent=2))


def main():
    args = parse_args(sys.argv)
    handle_args(args)
    #reader_type_map[args.command].handle_args(args)
    sys.exit(0)


if __name__ == "__main__":
    main()
