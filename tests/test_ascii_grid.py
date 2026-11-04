import os
import pytest

from dsprofile.lib import ASCIIGRIDReader

TEST_DATA_PATH = os.getenv("DSPROFILE_TEST_DATA_PATH")


@pytest.fixture
def ascii_grid_test_file(request):
    if TEST_DATA_PATH:
        test_dir = TEST_DATA_PATH
    else:
        base_dir = os.path.dirname(request.module.__file__)
        test_dir = os.path.join(base_dir, "data")
    return {
        "path": os.path.join(test_dir, "sample.asc"),
        "header": {
            "ncols": 3,
            "nrows": 2,
            "xllcorner": 100.0,
            "yllcorner": 200.0,
            "cellsize": 10.0,
            "nodata_value": -9999.0
        },
        "data": {
            "row_count": 2,
            "expected_row_count": 2
        }
    }


class TestASCIIGrid:
    def test_instance(self, ascii_grid_test_file):
        r = ASCIIGRIDReader(ascii_grid_test_file["path"])

        assert r.format == "ascii_grid"
        assert r.dataset["header"] == ascii_grid_test_file["header"]

    def test_read_dataset(self, ascii_grid_test_file):
        r = ASCIIGRIDReader(ascii_grid_test_file["path"])
        data = r.process()

        for key in ("header", "data"):
            assert data[key] == ascii_grid_test_file[key]
