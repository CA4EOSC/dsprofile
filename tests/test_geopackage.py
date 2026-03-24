import math
import random
import subprocess
import tempfile

from io import BytesIO
from shapely import Point

import geopandas as gpd
import pytest

from dsprofile.lib.geopackage import GeoPackageReader


def make_names(count):
    """
      Generate a sequence of names in ascending
      'powers' of A-Z: A,...,Z,AA,...,AZ,AAA,...
    """
    def exp26(i):
        seq = []
        i += 1
        while i != 0:
            i -= 1
            seq.insert(0, i%26)
            i //= 26

        if len(seq) == 0:
            seq = [0]
        return seq

    return ["".join(chr(65 + d) for d in exp26(i)) for i in range(abs(count))]


@pytest.fixture(scope="module")
def geometry_geodataframe():
    """
      Generate a GeoPandas GeoDataFrame with geometry col containing
      a sequence of Points having random (lat, long) coords
    """
    base_lat, base_long = 53.5, -2.25
    lat_band = random.uniform(25.0, 35.0)

    pcount = random.randint(160, 320)
    crs = "EPSG:4326"

    lat_longs = [(round(base_lat + math.sin(i*math.pi/(pcount/2))*lat_band, 2),
                  round(base_long + i*180/pcount, 2)) for i in range(pcount)]

    return gpd.GeoDataFrame({"names": make_names(pcount)}, geometry=[Point(c) for c in lat_longs], crs=crs)


@pytest.fixture(scope="module")
def elevation_geodataframe():
    """
      Generate a GeoPandas GeoDataFrame containing a sequence
      of random elevations
    """
    base_elev = 100
    elev_band = random.uniform(80, 120)

    pcount = random.randint(160, 320)

    elevations = [round(base_elev + math.sin(i*math.pi/(pcount/2))*elev_band, 2) for i in range(pcount)]

    return gpd.GeoDataFrame({"names": make_names(pcount), "Elevation": elevations})


@pytest.fixture(scope="module")
def multi_layer_tempfile(geometry_geodataframe, elevation_geodataframe):
    """
      Create a temporary file containing the geometry and elevation
      GeoDataframes as layers.
      Note that the `pyogrio` library underlying GeoPandas does not support
      writing multiple layers to a BytesIO buffer (as in `single_layer_buf`
      below) so a temp file is required here.
    """
    tmpfile = tempfile.NamedTemporaryFile(suffix=".gpkg")

    geometry_geodataframe.to_file(tmpfile.name, layer="Points", driver="GPKG")
    elevation_geodataframe.to_file(tmpfile.name, layer="Elevation", driver="GPKG")

    yield tmpfile
    tmpfile.close()


@pytest.fixture(scope="module")
def single_layer_buf(geometry_geodataframe):
    """
      Create a byte buffer containing a GeoDataFrame
    """
    buf = BytesIO()
    # Note it's necessary to specify a layer name for
    # even a single layer or a driver-specific arbitrary
    # layer name is used
    geometry_geodataframe.to_file(buf, layer="Points", driver="GPKG")
    buf.seek(0)
    yield buf
    buf.close()


var_name_map = {
    "Points": (("geometry", "geometry"), ("names", "str")),
    "Elevation": (("Elevation", "float64"), ("names", "str"))
}


class TestGeoPackage:
    def test_reader_instance(self, multi_layer_tempfile):
        """
          Can an instance of the GeoPackageReader be
          created and does it have the correct defaults?
        """
        inst = GeoPackageReader(multi_layer_tempfile.name)
        assert len(inst.layers) == 2

    def test_read_dataset_file(self, multi_layer_tempfile):
        """
          Does the output from reading a GeoPackage file
          have the expected form, values, and types?
        """
        inst = GeoPackageReader(multi_layer_tempfile.name)
        out = inst.process()
        for layer in out["layers"]:
            for name, dtype in var_name_map[layer["name"]]:
                assert name in layer["variables"]
                assert layer["variables"][name] == dtype

    def test_read_dataset_buf(self, single_layer_buf):
        """
          Does the output from reading a GeoPackage buffer
          have the expected form, values, and types?
        """
        inst = GeoPackageReader(single_layer_buf)
        assert len(inst.layers) == 1
        out = inst.process()
        for layer in out["layers"]:    # There's only one
            for name, dtype in var_name_map[layer["name"]]:
                assert name in layer["variables"]
                assert layer["variables"][name] == dtype

    def test_cli(self):
        """
          Can the command-line script be invoked using the
          GeoPackageReader's `format` attribute?
        """
        args = ["dsprofile", GeoPackageReader.format, "-h"]
        proc = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        sout, serr = proc.communicate()
        assert sout.startswith(b"usage")
        assert len(serr) == 0    # Should be an empty bytes: b""
        assert proc.returncode == 0

    def test_geometry(self, multi_layer_tempfile):
        """
          Does the Reader correctly identify the presence or absence
          of a geometry column?
        """
        inst = GeoPackageReader(multi_layer_tempfile.name)
        geom_out = inst.process()
        for layer in geom_out["layers"]:
            if layer["name"] == "Points":
                assert layer["geometry"] == "geometry"
            elif layer["name"] == "Elevation":
                assert layer["geometry"] == "None"
