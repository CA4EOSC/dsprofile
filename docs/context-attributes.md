# Context Attributes

Context Attributes allow arbitrary `JSON` objects to be associated with datasets.

This may be as simple as a single `{"key": value}` pair or may be an object which
provides extensive contextual metadata about a dataset, for example provenance
information.

In either case, the Context Attribute must be provided as a valid `JSON` definition.


## Syntax

To specify a single `{"key": value}` pair, add this directly at the command-line
with the `--context-attribute` option:

```
$ dsprofile --context-attribute '{"key": "value"}' ...
```

Many attributes may be specified in a single context object provided at
the command line, for example:

```
$ dsprofile --context-attribute '{"key1": "value1", "key2": 5.12, "key3": [1.0, 2.0, 3.0], "key4": {"nested_key": "nested_value"}}' ...
```

A more convenient option for providing multiple attributes is to store these
in a file. For example, the file `attributes.json` contains the following `JSON`
object.

```json
{
  "key1": "value1",
  "key2": 5.12,
  "key3": [1.0, 2.0, 3.0],
  "key4": {"nested_key": "nested_value"}
}
```

This file may be redirected to the `--context-attribute` option at the command line:

```
$ dsprofile --context-attribute "$(<attributes.json)" ...
```

## Output

Context attributes added to a dataset will be located in the `metadata` section of the
output as the `attributes` value. For example:

```json
{
  "metadata": {
    "env": {
      "created": "2026-05-01 13:18:55",
      "command": "dsprofile netcdf tests/data/test.nc",
      "version": "0.2.0",
      "os": "Linux"
    },
    "file": {
      "name": "tests/data/test.nc",
      "size": 8192,
      "digest": "b5441b97fd11a723816c7f5eb082fd0cfadce7b8af46d934fd764db2caa03b2b"
    },
    "attributes": {
        "key1": "value1",
        "key2": 5.12,
        "key3": [1.0, 2.0, 3.0],
        "key4": {"nested_key": "nested_value"}
    },
  "content": <omitted>
  }
}
```
