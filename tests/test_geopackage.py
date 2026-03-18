import os

import pytest

from dsprofile.lib.geopackage import GeoPackageReader


TEST_DATA_PATH = os.getenv("DSPROFILE_TEST_DATA_PATH")


@pytest.fixture
def synthetic_test_file(request):
    if TEST_DATA_PATH:
        test_dir = TEST_DATA_PATH
    else:
        base_dir = os.path.dirname(request.module.__file__)
        test_dir = os.path.join(base_dir, "data")
    return {
        "path": os.path.join(test_dir, "test.gpkg")
        # TODO
    }


class TestGeoPackage:
    def test_reader_instance(self, synthetic_test_file):
        """
          Can an instance of the GeoPackageReader be
          created and does it have the correct defaults?
        """

    def test_read_dataset(self, synthetic_test_file):
        """
          Can a GeoPackage file be opened correctly?
        """
