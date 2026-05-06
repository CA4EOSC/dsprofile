import os

import pytest


TEST_DATA_PATH = os.getenv("DSPROFILE_TEST_DATA_PATH")


@pytest.fixture
def synthetic_test_file(request):
    if TEST_DATA_PATH:
        test_dir = TEST_DATA_PATH
    else:
        base_dir = os.path.dirname(request.module.__file__)
        test_dir = os.path.join(base_dir, "data")
    return {
        "path": os.path.join(test_dir, "test.nc"),
        "groups": ['/top01',
                   '/top02',
                   '/top01/nest_a',
                   '/top01/nest_b',
                   '/top01/nest_a/nest_a_01',
                   '/top01/nest_a/nest_a_02',
                   '/top01/nest_b/nest_b_01',
                   '/top01/nest_b/nest_b_02',
                   '/top01/nest_b/nest_b_03']
    }
