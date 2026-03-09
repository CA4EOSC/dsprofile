![ci-workflow](https://github.com/CA4EOSC/dsprofile/actions/workflows/ci.yml/badge.svg)

# Dataset Profile

## Overview

A utility to describe the structure of datasets in netCDF, GeoTiff,
and ESRI Shapefile format.

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

```
usage: dsprofile [-h] {netcdf,geotiff,shape} ...

Describes datasets in a variety of formats

options:
  -h, --help           show this help message and exit

Dataset formats:
  {netcdf,geotiff,shape}
    netcdf             Extracts metadata from netCDF4 files
    geotiff            Extracts metadata from GeoTIFF files
    shape              Extracts metadata from ESRI Shape files
```

## NetCDF Options

Reads a netCDF4 file and reports the group structure and information
about any dimensions, variables, and attributes that are defined.

```
usage: dsprofile netcdf [-h] [-o {category,group}] [-e <group0>,<group1>,...] [-m] [-d] filename

positional arguments:
  filename

options:
  -h, --help            show this help message and exit
  -o {category,group}, --order-by {category,group}
                        (default group)
  -e <group0>,<group1>,..., --exclude-groups <group0>,<group1>,...
                        Exclude each of the named <group> arguments
  -m, --omit-metadata   Output only netCDF file contents, not file metadata
  -d, --omit-digest     Do not include a hash digest in file metadata
```

The `--order-by` option allows the resulting output to be arranged in one of two ways:

    1. By `group` creates a listing of dimensions, variables, and attributes for
       each netCDF group within a file.
    2. By `category` creates a listing of the properties of each group organised into
       separate examples for each category of dimension, variable, and attribute.

The `--omit-digest` option prevents calculation of a SHA256 hash for the processed file.
This may be desirable for very large files or test workflows to avoid the potentially
time-consuming hashing operation.

### NetCDF Example

For example, to report on the contents of the netCDF4 file `test.nc` using the default
output options...

```
$ dsprofile netcdf test.nc
```

## GeoTiff Options

```
usage: dsprofile geotiff [-h] [-m] [-d] filename

positional arguments:
  filename

options:
  -h, --help           show this help message and exit
  -m, --omit-metadata  Output only GeoTIFF file contents, not file metadata
  -d, --omit-digest    Do not include a hash digest in file metadata
```

## ESRI Shapefile Options

```
usage: dsprofile shape [-h] [-m] [-d] filename

positional arguments:
  filename

options:
  -h, --help           show this help message and exit
  -m, --omit-metadata  Output only Shape file contents, not file metadata
  -d, --omit-digest    Do not include a hash digest in file metadata
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
