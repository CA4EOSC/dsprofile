import os

import pytest
import rasterio as rio

from dsprofile.lib.readers.tiff import GeoTIFFReader


TEST_DATA_PATH = os.getenv("DSPROFILE_TEST_DATA_PATH")


@pytest.fixture
def geotiff_test_file(request):
    if TEST_DATA_PATH:
        test_dir = TEST_DATA_PATH
    else:
        base_dir = os.path.dirname(request.module.__file__)
        test_dir = os.path.join(base_dir, "data")
    return {
        "path": os.path.join(test_dir, "GeogToWGS84GeoKey5.tif"),
        "meta": {
            "shape": {
                "width": 101,
                "height": 101
            },
            "bands": {1: "uint8"},
            "bounds": {
                "left": 8.999654601821101,
                "bottom": 51.9999732301211,
                "right": 9.0024601573789,
                "top": 52.0027787856789
            }
        }
    }


class TestGeoTIFF:
    def test_reader_instance(self, geotiff_test_file):
        """
          Can an instance of the GeoTIFFReader be created
          with the expected default attributes?
        """
        r = GeoTIFFReader(geotiff_test_file["path"])
        assert r.format == GeoTIFFReader.format

    def test_dataset_fileops(self, geotiff_test_file):
        """
          Can a GeoTIFF file be opened correctly, and
          does the finalizer correctly close the file
          when manually invoked?
        """
        r = GeoTIFFReader(geotiff_test_file["path"])
        assert isinstance(r.tif, rio.io.DatasetReader)
        assert r._finalizer.alive
        tref = r.tif
        assert not tref.closed  # Our tiff file is open...
        r.close()  # ...the finalizer is invoked...
        assert tref.closed  # ...so the file must be closed

    def test_read_dataset(self, geotiff_test_file):
        """
          Are the expected metadata values correctly
          retrieved from the test GeoTIFF file?
        """
        r = GeoTIFFReader(geotiff_test_file["path"])
        data = r.process()
        for k, v in geotiff_test_file["meta"].items():
            assert data[k] == v
