import pathlib
import sys
import weakref

from collections.abc import Sequence

from dsprofile.lib.reader import Reader

import netCDF4 as nc


class NetCDFReader(Reader):
    """
      Defines a reader type for NetCDF4-based datasets.
      Note that the underlying library may include support
      for other (and non-HDF based) NetCDF formats, but this assumes
      the availability of NetCDF4 primitives.
    """

    format = "netcdf"

    def __init__(self, filename, order_by="group", exclude=None):
        self.ds = self.__class__.read_dataset(filename)
        self._finalizer = weakref.finalize(self, self.finalize_close, self.ds)
        self.order_by = order_by
        # Note that the order is significant here
        # as str is a Sequence type
        if not exclude:
            self.exclude_groups = []
        elif isinstance(exclude, str):
            self.exclude_groups = [exclude]
        elif issubclass(type(exclude), Sequence):
            self.exclude_groups = exclude

    @staticmethod
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
            ds.close()
            sys.exit(1)

        return ds

    @staticmethod
    def finalize_close(ncdf):
        """
          An out-of-scope handler (usually) invoked by weakref.finalize
          which should ensure that any resources acquired by this
          instance are correctly returned before GC.
        """
        if isinstance(ncdf, nc.Dataset) and ncdf.isopen():
            ncdf.close()

    def close(self):
        if self._finalizer.alive:
            self._finalizer()

    def walk_groups_breadth_first(self, ds=None):
        if not ds:
            ds = self.ds
        yield (g for g in ds.groups.values() if g.path not in self.exclude_groups)
        for group in ds.groups.values():
            if group.path in self.exclude_groups:
                continue
            yield from self.walk_groups_breadth_first(group)

    def walk_groups_depth_first(self, ds=None):
        if not ds:
            ds = self.ds
        for group in ds.groups.values():
            if group.path in self.exclude_groups:
                continue
            yield from self.walk_groups_depth_first(group)
        yield (g for g in ds.groups.values() if g.path not in self.exclude_groups)

    walk_func_map = {
        "breadth": walk_groups_breadth_first,
        "depth": walk_groups_depth_first
    }

    def walk_groups(self, ds=None, order="breadth"):
        return self.walk_func_map[order](self, ds)

    def gather_by_group(self):
        """
          A categorisation of dimensions, variables, and
          attributes defined in the <ds> Dataset argument,
          ordered by the group to which they belong.
        """
        dims = self.describe_dimensions()
        ncvars = self.describe_variables()
        attrs = self.describe_attributes()
        by_group = {"/": {
            "dimensions": dims["/"],
            "variables": ncvars["/"],
            "attributes": attrs["/"]
            }
        }
        for groups in self.walk_groups():
            for group in groups:
                by_group[group.path] = {
                    "dimensions": dims[group.path],
                    "variables": ncvars[group.path],
                    "attributes": attrs[group.path]
                }

        return by_group

    def gather_by_type(self):
        """
          A categorisation of dimensions, variables, and
          attributes defined in the <ds> Dataset argument,
          ordered by type.
        """
        return {
            "dimensions": self.describe_dimensions(),
            "variables": self.describe_variables(),
            "attributes": self.describe_attributes()
        }

    process_func_map = {
        "category": gather_by_type,
        "group": gather_by_group
    }

    def describe_dimensions(self):
        dimensions = {}

        dimensions['/'] = {d.name: {"size": d.size} for d in self.ds.dimensions.values()}
        for groups in self.walk_groups():
            for group in groups:
                dimensions[group.path] = {d.name: {"size": d.size} for d in group.dimensions.values()}

        return dimensions

    def describe_variables(self):
        variables = {}
        variables['/'] = {v.name: {"dtype": v.dtype.name,
                                   "dimensions": v.dimensions,
                                   "fill_value": str(v.get_fill_value())}
                                   for v in self.ds.variables.values()}
        for groups in self.walk_groups():
            for group in groups:
                variables[group.path] = {v.name: {"dtype": v.dtype.name,
                                         "dimensions": v.dimensions,
                                         "fill_value": str(v.get_fill_value())}
                                         for v in group.variables.values()}
        return variables

    def describe_attributes(self):
        attrs = {}
        attrs['/'] = {"group": [a for a in self.ds.ncattrs()],
                      "vars": {v.name: [a for a in v.ncattrs()] for v in self.ds.variables.values()}
                     }
        for groups in self.walk_groups():
            for group in groups:
                attrs[group.path] = {"group": [a for a in group.ncattrs()],
                                     "vars": {v.name: [a for a in v.ncattrs()] for v in group.variables.values()}
                                    }
        return attrs

    def process(self):
        return self.process_func_map[self.order_by](self)

    @classmethod
    def build_subparser(cls, sp):
        parser = sp.add_parser(cls.format,
                               help="Extracts metadata from netCDF4 files")
        parser.add_argument("filename", type=pathlib.Path)
        parser.add_argument("-o", "--order-by", choices=["category", "group"],
                            default="group", help="(default group)")
        parser.add_argument("-e", "--exclude-groups", metavar="<group0>,<group1>,...",
                            help="Exclude each of the named <group> arguments")
        parser.add_argument("-m", "--omit-metadata", action="store_true",
                            help="Output only netCDF file contents, not file metadata")
        parser.add_argument("-d", "--omit-digest", action="store_true",
                            help="Do not include a hash digest in file metadata")
        return parser

    @classmethod
    def handle_args(cls, args):
        if args.filename.is_dir():
            print(f"A valid file is required not directory '{args.filename}'",
                  file=sys.stderr)
            sys.exit(1)

        exclude = []
        if hasattr(args, "exclude_groups"):
            exclude = args.exclude_groups.split(',') if args.exclude_groups else []

        ctor_args = [args.filename, args.order_by, exclude]
        ctor_kwargs = {}

        return ctor_args, ctor_kwargs
