import json
import os
import subprocess

import pytest

from dsprofile.lib.netcdf import NetCDFReader



@pytest.fixture
def context_attribute():
    return {
        "key1": "value1",
        "key2": 5.12,
        "key3": [1.0, 2.0, 3.0],
        "key4": {"nested_key": "nested_value"}
    }


class TestContextAttribute:
    def test_attrs_require_metadata(self):
        """
          Do contradictory arguments `-context-attribute` and
          `--omit-metadata` result in the expected error?
        """
        # $ dsprofile -a '{"key": "value"}' netcdf /dev/null
        args = ["dsprofile", "--context-attribute", '{"key": "value"}', "--omit-metadata", NetCDFReader.format, "/dev/null"]
        proc = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        sout, serr = proc.communicate()

        assert serr.startswith(b"Metadata profile cannot be omitted")
        assert len(sout) == 0    # Should be an empty bytes: b""
        assert proc.returncode == 1

    def test_context_attr_single(self, synthetic_test_file):
        """
          Can a valid context attribute be parsed and
          included in the metadata profile?
        """
        args = ["dsprofile", "--context-attribute", '{"key": "value"}', NetCDFReader.format, synthetic_test_file["path"]]
        proc = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        sout, serr = proc.communicate()
        output = json.loads(sout)

        assert output["metadata"]["attributes"]["key"] == "value"

    def test_context_attr_complex(self, context_attribute, synthetic_test_file):
        """
          Can a valid context attribute object be parsed and
          included in the metadata profile?
        """
        args = ["dsprofile", "--context-attribute", json.dumps(context_attribute), NetCDFReader.format, synthetic_test_file["path"]]
        proc = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        sout, serr = proc.communicate()
        output = json.loads(sout)

        assert len(output["metadata"]["attributes"]) == len(context_attribute)
        assert output["metadata"]["attributes"]["key1"] == context_attribute["key1"]
        assert output["metadata"]["attributes"]["key2"] == context_attribute["key2"]
        assert output["metadata"]["attributes"]["key3"] == context_attribute["key3"]
        assert output["metadata"]["attributes"]["key4"] == context_attribute["key4"]
