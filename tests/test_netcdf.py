import os
import subprocess

import pytest

from dsprofile.lib.netcdf import NetCDFReader


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
        "groups": [ '/top01',
                    '/top02',
                    '/top01/nest_a',
                    '/top01/nest_b',
                    '/top01/nest_a/nest_a_01',
                    '/top01/nest_a/nest_a_02',
                    '/top01/nest_b/nest_b_01',
                    '/top01/nest_b/nest_b_02',
                    '/top01/nest_b/nest_b_03']
    }


class TestNetCDF:
    def test_reader_instance(self, synthetic_test_file):
        """
          Can an instance of the NetCDFReader be created
          and does it have the correct defaults?
        """
        r = NetCDFReader(synthetic_test_file["path"])
        assert r.format == NetCDFReader.format
        assert r.order_by == "group"
        assert r.exclude_groups == []

    def test_read_dataset(self, synthetic_test_file):
        """
          Can a netCDF4 file be opened correctly?
        """
        ds = NetCDFReader.read_dataset(synthetic_test_file["path"])
        assert ds.data_model == "NETCDF4"

    def test_walk_groups(self, synthetic_test_file):
        """
          Are groups correctly identified and appear
          in the expected order?
        """
        r = NetCDFReader(synthetic_test_file["path"])
        _ = r.process()
        groupnames = [group.path for groups in r.walk_groups(r.ds) for group in groups]
        for idx in range(len(groupnames)):
            assert groupnames[idx] == synthetic_test_file["groups"][idx]

    def test_exclude_groups(self, synthetic_test_file):
        """
          Are group paths excluded from the search
          correctly omitted?
        """
        exclusion = "/top01/nest_b"
        r = NetCDFReader(synthetic_test_file["path"], exclude=exclusion)
        groupnames = [group.path for groups in r.walk_groups(r.ds) for group in groups]
        filtered_groups = [group for group in synthetic_test_file["groups"] if not group.startswith(exclusion)]
        for idx in range(len(groupnames)):
            assert groupnames[idx] == filtered_groups[idx]

    def test_order_by(self, synthetic_test_file):
        """
          Do the orderings by `group` and by `category` produce
          the expected output?
        """
        r_cat = NetCDFReader(synthetic_test_file["path"], order_by="category")
        out = r_cat.process()
        for category in ("dimensions", "variables", "attributes"):
            assert category in out
        
        r_grp = NetCDFReader(synthetic_test_file["path"], order_by="group")
        out = r_grp.process()
        for group in synthetic_test_file["groups"]:
            assert group in out

    def test_cli(self):
        """
          Can the command-line script be invoked using the
          NetCDFReader's `format` attribute?
        """
        args = ["dsprofile", NetCDFReader.format, "-h"]
        proc = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        sout, serr = proc.communicate()
        assert sout.startswith(b"usage")
        assert len(serr) == 0    # Should be an empty bytes: b""
        assert proc.returncode == 0
