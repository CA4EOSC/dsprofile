import datetime
import os
import sys

from importlib.metadata import version

import netCDF4 as nc


def read_dataset(filename):
    """
      Handle OSError, PermissionError, FileNotFoundError neatly
      Inform neatly for non-netCDF4 files
      Allow all other exceptions to raise unhandled
    """

    try:
        ds = nc.Dataset(filename, 'r')
    except (OSError, PermissionError, FileNotFoundError) as e:
        print(f"{e.strerror} for file '{filename}'", file=sys.stderr)
        sys.exit(1)

    if ds.data_model != "NETCDF4":
        print(f"File '{filename}' has format '{ds.data_model}', "
              f"not 'NETCDF4' as required", file=sys.stderr)
        sys.exit(1)

    return ds


def make_file_profile(ctx):
    try:
        stat = os.stat(ctx.filename)
    except (OSError, PermissionError, FileNotFoundError) as e:
        print(f"{e.strerror} for file '{ctx.filename}'", file=sys.stderr)
        sys.exit(1)

    origin = {
        "env": {
            "created": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"),
            "command": " ".join([os.path.basename(sys.argv[0])] + sys.argv[1:]),
            "version": version(__package__),
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
        with open(ctx.filename, 'rb') as fp:
            h.update(fp.read())
        origin["file"]["digest"] = h.hexdigest()

    return origin
