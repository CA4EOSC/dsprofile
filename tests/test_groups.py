import os

import pytest

from ncmetadata.reader import (
    exclude_groups,
    read_dataset,
    walk_groups
)


TEST_DATA_PATH = os.getenv("NCDF_TEST_DATA_PATH", "tests/data")

@pytest.fixture
def synthetic_test_file():
    return {
        "path": os.path.join(TEST_DATA_PATH, "test.nc"),
        "groups": ['/top01/nest_a/nest_a_01',
                   '/top01/nest_a/nest_a_02',
                   '/top01/nest_a',
                   '/top01/nest_b/nest_b_01',
                   '/top01/nest_b/nest_b_02',
                   '/top01/nest_b/nest_b_03',
                   '/top01/nest_b',
                   '/top01',
                   '/top02',
                   '/']
    }


class TestGroups:
    def test_read_dataset(self, synthetic_test_file):
        """
          Can a netCDF4 file be opened correctly?
        """
        ds = read_dataset(synthetic_test_file["path"])

    def test_walk_groups(self, synthetic_test_file):
        """
          Are groups correctly identified and appear
          in the expected order?
        """
        ds = read_dataset(synthetic_test_file["path"])
        groupnames = [group.path for group in walk_groups(ds)]
        for idx in range(len(groupnames)):
            assert groupnames[idx] == synthetic_test_file["groups"][idx]

    def test_exclude_groups(self, synthetic_test_file):
        """
          Are group paths excluded from the search
          correctly omitted?
        """
        ds = read_dataset(synthetic_test_file["path"])
        exclusion = "/top01/nest_b"
        exclude_groups.append(exclusion)
        groupnames = [group.path for group in walk_groups(ds)]
        filtered_groups = [group for group in synthetic_test_file["groups"] if not group.startswith(exclusion)]
        for idx in range(len(groupnames)):
            assert groupnames[idx] == filtered_groups[idx]
