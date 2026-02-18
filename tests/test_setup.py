import os
from packaging import version

import pytest


min_version_map = {
    "netCDF4": version.parse("1.7.0")
}


class TestSetup:
    def test_lib_versions(self):
        """
          Are the required libraries present and adequate versions?
        """
        import importlib
        for libname, semver in min_version_map.items():
            lib = importlib.import_module(libname)
            assert version.parse(lib.__version__) >= semver
        
