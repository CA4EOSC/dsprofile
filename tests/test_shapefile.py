import os

import pytest
from fiona import Collection
import numpy as np

from dsprofile.lib import ShapefileReader


TEST_DATA_PATH = os.getenv("DSPROFILE_TEST_DATA_PATH", "tests/data")


@pytest.fixture
def shape_test_file():
    return {
        "path": os.path.join(TEST_DATA_PATH, "SJER_crop2.shp"),
        "meta": {
            "bounds": [
              255209.5107915717,
              4108471.237186788,
              257532.73265945335,
              4110975.960763098
            ],
            "features": [
              {
                "type": "Polygon",
                "coordinates": 7,
                "properties": {
                  "id": 1
                }
              }
            ],
            "units": "metre",
            "factor": 1.0,
            "crs": "EPSG:32611"
        }
    }


class TestShapefile:
    def test_instance(self, shape_test_file):
        """
          Can an instance of the ShapefileReader be created
          with the expected default attributes?
        """
        s = ShapefileReader(shape_test_file["path"])
        assert s.format == ShapefileReader.format
        assert s.shp.driver.lower() == "esri shapefile"

    def test_read_dataset(self, shape_test_file):
        """
          Are the expected metadata values correctly
          retrieved from the test Shape file?
        """
        r = ShapefileReader(shape_test_file["path"])
        assert isinstance(r.shp, Collection)
        data = r.process()

        for key in shape_test_file["meta"]:
            assert key in data

        assert np.allclose(data["bounds"], shape_test_file["meta"]["bounds"])
        assert len(data["features"]) == len(shape_test_file["meta"]["features"])
        direct_attrs = ("units", "factor", "crs")
        for attr in direct_attrs:
            assert data[attr] == shape_test_file["meta"][attr]
