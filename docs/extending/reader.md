# Adding a dataset `Reader` to `dsprofile`

Adding a reader for a new dataset type requires creating a subtype
of the [`Reader` abstract base class](../reference/reader.md) and
implementing versions of the required methods which perform operations
appropriate to that type.

## The "format" (`subclass_type_key`) attribute

Each class derived from `Reader` must provide a class attribute
named `format` containing a string serving as a tag for the dataset
handled by that class. For example, the `MyData` type might have
a `format` attribute named "mydata", as demonstrated below:

``` python
from dsprofile.lib.reader import Reader

class MyData(Reader):
    format = "mydata"
    ...
```

The value provided in `format` will be used as the command name
that is provided to `dsprofile` on the command line to identify
this dataset type. As such, it must not contain spaces or other
characters which have significance to the shell.

Although the default name of this attribute is `format`, it may be
changed via the `Reader.subclass_type_key`. Note that any such change
affects *all* derived classes, including those which already exist. 

## `Reader` methods

### `<classmethod> build_subparser(cls, sp):`

::: dsprofile.lib.reader.Reader.build_subparser

This method is responsible for adding any type-specific options
to the command-line argument parser.

In particular, it must add a subcommand key which identifies this
`Reader` type when invoking `dsprofile` from the command-line. For
example, to create a new subcommand for the `MyData` dataset reader
whose `format` tag described above is "mydata", use the following:

``` python
parser = sp.add_parser(cls.format, help="Read datasets in mydata format")
```

This `Reader` type will then be available on the command-line with the
"mydata" subcommand, for example:

```
$ dsprofile mydata /path/to/mydata.file
```

### `<classmethod> handle_args(cls, args) -> tuple[list, dict]:`

::: dsprofile.lib.reader.Reader.handle_args

### `process(self) -> dict:`

::: dsprofile.lib.reader.Reader.process

## Resource ownership

It is important to note that `Reader` types are responsible for
managing any resources such as file handles or remote access state
that are used in reading their datasets.

The recommended way to manage such resources is using the `weakref`
module's [finalize](https://docs.python.org/3/library/weakref.html#finalizer-objects)
method to register a handler appropriate to the type.
