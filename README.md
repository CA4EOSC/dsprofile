# NetCDF Metadata

## Overview

A utility to describe the structure of NetCDF4 datasets.

Reads a NetCDF4 file and reports the group structure and information
about any dimensions, variables, and attributes that are defined.

## Installation

Build and install the package with...

```bash
$ python -m pip install .
```

The optional test suite may be installed and run with:

```bash
$ python -m pip install .[test]
$ pytest --cov=ncmetadata tests
```

## Usage

```bash
usage: dsprofile [-h] {netcdf,tiff,shape} ...

Describes datasets in a variety of formats

options:
  -h, --help           show this help message and exit

Dataset formats:
  {netcdf,tiff,shape}
    netcdf             Extracts metadata from netCDF4 files
    tiff               Extracts metadata from GeoTIFF files
    shape              Extracts metadata from ESRI Shape files
```

## NetCDF Options

```bash
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

```bash
$ dsprofile netcdf test.nc
```

## GeoTiff Options

## ESRI Shapefile Options
