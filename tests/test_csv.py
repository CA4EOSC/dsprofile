import os
import pytest

from dsprofile.lib import CSVReader

TEST_DATA_PATH = os.getenv("DSPROFILE_TEST_DATA_PATH")


@pytest.fixture
def csv_test_file(request):
    if TEST_DATA_PATH:
        test_dir = TEST_DATA_PATH
    else:
        base_dir = os.path.dirname(request.module.__file__)
        test_dir = os.path.join(base_dir, "data")
    return {
        "path": os.path.join(test_dir, "sample.csv"),
        "columns": ["id", "name", "value"],
        "rows": 2
    }


class TestCSV:
    def test_instance(self, csv_test_file):
        r = CSVReader(csv_test_file["path"])

        assert r.format == "csv"
        assert len(r.dataset) == 2
        assert r.dataset[0]["name"] == "alpha"

    def test_read_dataset(self, csv_test_file):
        r = CSVReader(csv_test_file["path"])
        data = r.process()

        assert "dataset" in data
        assert "alpha" in data["dataset"]
        for col in csv_test_file["columns"]:
            assert col in data["dataset"]
            