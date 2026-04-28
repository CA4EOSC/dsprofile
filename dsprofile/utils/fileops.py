"""
  General (ie. not type-specific) utility functions used
  by the dsprofile framework and readers.
"""
import datetime
import json
import os
import sys

from dsprofile import config
from importlib.metadata import version


def make_file_profile(ctx, context_attribute=None) -> dict:
    """
      Returns a summary of the file used as a command-line argument
      and useful metadata about the execution environment.
    """
    try:
        """
          Note that where "--omit-metadata" is not provided, this operation
          detects ENOENT and EPERM files *before* any type-specific
          constructor in Reader types.
        """
        stat = os.stat(ctx.filename)
    except (OSError, PermissionError, FileNotFoundError) as e:
        print(f"{e.strerror} for file '{ctx.filename}'", file=sys.stderr)
        sys.exit(1)

    origin = {
        "env": {
          "created": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"),
          "command": " ".join([os.path.basename(sys.argv[0])] + sys.argv[1:]),
          "version": version(config.PROGNAME),
          "os": os.uname().sysname
        },
        "file": {
          "name": str(ctx.filename),
          "size": stat.st_size
        }
    }
    if not ctx.omit_digest:
        from hashlib import sha256
        h = sha256()
        try:
            with open(ctx.filename, 'rb') as fp:
                h.update(fp.read())
        except (PermissionError, FileNotFoundError, OSError) as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        origin["file"]["digest"] = h.hexdigest()

    if context_attribute:
        try:
            ctx_attr = json.loads(context_attribute)
        except json.decoder.JSONDecodeError as e:
            print(f"Invalid context attribute: {e.msg}", file=sys.stderr)
            sys.exit(1)

        origin["attributes"] = ctx_attr

    return origin
