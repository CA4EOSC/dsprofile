![ci-workflow](https://github.com/CA4EOSC/dsprofile/actions/workflows/ci.yml/badge.svg)

# Dataset Profile

## Overview

A utility to create profiles of geospatial datasets in a range of formats to assist FAIRification.

For full documentation, please see [the DSprofile documentation](https://ca4eosc.github.io/dsprofile).

## Installation

Build and install the package with...

```
$ python -m pip install .
```

The optional test suite may be installed and run with:

```
$ python -m pip install .[test]
$ pytest --cov=dsprofile tests
```

## Usage

```bash
usage: dsprofile [-h] [-m] [-d] [-l <level>] [-a <attribute>] {netcdf,geotiff,shape,geopackage} ...

Describes datasets in a variety of formats

options:
  -h, --help            show this help message and exit
  -m, --omit-metadata   Output only file contents, not file metadata
  -d, --omit-digest     Do not include a hash digest in file metadata
  -l <level>, --log-level <level>
                        Specify the minimal log level
  -a <attribute>, --context-attribute <attribute>
                        Add a JSON object containing {attribute: value} pair(s)
                        to metadata profile

Dataset formats:
  {netcdf,geotiff,shape,geopackage}
    netcdf              Extracts metadata from netCDF4 files
    geotiff             Extracts metadata from GeoTIFF files
    shape               Extracts metadata from ESRI Shape files
    geopackage          Extracts metadata from GeoPackage files

For more information, see ca4eosc.github.io/dsprofile
```

The `--omit-digest` option prevents calculation of a SHA256 hash for the processed file.
This may be desirable for very large files or test workflows to avoid the potentially
time-consuming hashing operation.

## Reader-specific options

### NetCDF Options

Reads a netCDF4 file and reports the group structure and information
about any dimensions, variables, and attributes that are defined.

```
usage: dsprofile netcdf [-h] [-o {category,group}] [-e <group0>,<group1>,...] filename

positional arguments:
  filename

options:
  -h, --help            show this help message and exit
  -o {category,group}, --order-by {category,group}
                        (default group)
  -e <group0>,<group1>,..., --exclude-groups <group0>,<group1>,...
                        Exclude each of the named <group> arguments
```

The `--order-by` option allows the resulting output to be arranged in one of two ways:

    1. By `group` creates a listing of dimensions, variables, and attributes for
       each netCDF group within a file.
    2. By `category` creates a listing of the properties of each group organised into
       separate examples for each category of dimension, variable, and attribute.

#### NetCDF Example

For example, to report on the contents of the netCDF4 file `test.nc` using the default
output options...

```
$ dsprofile netcdf test.nc
```

### GeoTiff Options

```bash
usage: dsprofile geotiff [-h] filename

positional arguments:
  filename

options:
  -h, --help           show this help message and exit
```

### ESRI Shapefile Options

```bash
usage: dsprofile shape [-h] filename

positional arguments:
  filename

options:
  -h, --help           show this help message and exit
```

A Shapefile may be read by opening any of its components, for example...

```
$ dsprofile shape shapefile.shp
```
...is equivalent to...

```
$ dsprofile shape shapefile.dbf
```
Note however that where a hex digest of a hash is included in the output,
this will refer only to file provided as a command-line argument.

### GeoPackage Options

```bash
usage: dsprofile geopackage [-h] filename

positional arguments:
  filename

options:
  -h, --help  show this help message and exit
```
