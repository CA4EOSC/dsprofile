from ncmetadata.util import (
    read_dataset
)

exclude_groups = []



def walk_groups_breadth_first(ds):
    yield ds.groups.values()
    for group in ds.groups.values():
        yield from walk_groups_breadth_first(group)


def walk_groups_depth_first(ds):
    for group in ds.groups.values():
        yield from walk_groups_depth_first(group)
    yield ds.groups.values()


def walk_groups_ordered(ds):
    for group in ds.groups.values():
        if group.path in exclude_groups:
            continue
        yield from walk_groups_ordered(group)
    yield ds


walk_func_map = {
    "breadth": walk_groups_breadth_first,
    "depth": walk_groups_depth_first,
    "ordered": walk_groups_ordered
}


def walk_groups(ds, order="ordered"):
    return walk_func_map[order](ds)


def describe_dimensions(ds):
    dimensions = {}

    for group in walk_groups(ds):
        dimensions[group.path] = {d.name: {"size": d.size} for d in group.dimensions.values()}

    return dimensions


def describe_variables(ds):
    variables = {}
    for group in walk_groups(ds):
        variables[group.path] = {v.name: {"dtype": v.dtype.name,
                                           "dimensions": v.dimensions,
                                           "fill_value": str(v.get_fill_value())}
                                 for v in group.variables.values()}
    return variables


def describe_attributes(ds):
    attrs = {}
    for group in walk_groups(ds):
        attrs[group.path] = {"group": [a for a in group.ncattrs()],
                             "vars": {v.name: [a for a in v.ncattrs()] for v in group.variables.values()}
                            }

    return attrs


def gather_by_group(ds):
    """
      A categorisation of dimensions, variables, and
      attributes defined in the <ds> Dataset argument,
      ordered by the group to which they belong.
    """
    dims = describe_dimensions(ds)
    ncvars = describe_variables(ds)
    attrs = describe_attributes(ds)
    by_group = {}
    for group in walk_groups(ds):
        by_group[group.path] = {
            "dimensions": dims[group.path],
            "variables": ncvars[group.path],
            "attributes": attrs[group.path]
        }

    return by_group


def gather_by_type(ds):
    """
      A categorisation of dimensions, variables, and
      attributes defined in the <ds> Dataset argument,
      ordered by type.
    """
    return {
        "dimensions": describe_dimensions(ds),
        "variables": describe_variables(ds),
        "attributes": describe_attributes(ds)
    }

process_func_map = {
    "category": gather_by_type,
    "group": gather_by_group
}

def process_file(filename, order_by, exclude):
    global exclude_groups
    exclude_groups = exclude
    ds = read_dataset(filename)
    return process_func_map[order_by](ds)
