import logging
import os
import subprocess

import pytest

from dsprofile import config
from dsprofile.lib import Reader
from dsprofile.utils import logged


class DummyLoggingReader(Reader):
    format = "dummy"

    # Required abstract method
    def handle_args(self):
        pass

    # Required abstract method
    def build_subparser(self):
        pass

    def not_log_meth(self):
        return {}

    @logged
    def process(self):
        return {}

    @logged("DEBUG")
    def debug_log_meth(self):
        return {}

    @logged(time=True)
    def time_log_meth(self):
        return {}

    @logged("ERROR", time=True)
    def time_level_log_meth(self):
        return {}


@pytest.fixture(scope="module", autouse=True)
def configure_logging():
    config.log_config()


class TestLogging:
    def test_log_config(self, caplog):
        """
          Is the logger returned from config identical to that
          expected when explicitly retrieved from the logging
          module?
        """
        conf_logger = config.getLogger()
        prog_logger = logging.getLogger(config.PROGNAME)
        assert conf_logger == prog_logger

    def test_instance_log(self, caplog):
        """
          Does the `logged` decorator emit a log message
          at the correct level?
        """
        dr = DummyLoggingReader()

        # A single INFO message with the expected text should appear
        with caplog.at_level(logging.DEBUG, logger=config.PROGNAME):
            dr.process()
        assert len(caplog.records) == 1
        assert caplog.records[0].msg == f"{dr.__class__.__qualname__}.process"
        assert caplog.records[0].levelname == "INFO"

        # No further message should appear due to logger level
        with caplog.at_level(logging.CRITICAL, logger=config.PROGNAME):
            dr.process()
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "INFO"

        # No further message should appear due to meth not being @logged
        with caplog.at_level(logging.DEBUG, logger=config.PROGNAME):
            dr.not_log_meth()
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "INFO"

        caplog.records.clear()

        # A single DEBUG message with the expected text should appear
        with caplog.at_level(logging.DEBUG, logger=config.PROGNAME):
            dr.debug_log_meth()
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "DEBUG"

    def test_log_cli(self, caplog):
        """
          Does the cli `--log-level` option exist and support the
          expected log levels?

          NB. This doesn't test *use* of the --log-level arg due
          to this requiring a full run with dataset input.
        """
        os.environ["DSPROFILE_USE_LOGGING"] = "1"
        args = ["dsprofile", "--log-level=NONEXIST", "netcdf", "filename.nc"]
        proc = subprocess.Popen(args,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        with caplog.at_level(logging.DEBUG, logger=config.PROGNAME):
            _, serr = proc.communicate()
        assert serr.startswith(b"Invalid log level 'NONEXIST'")

        for level in logging.getLevelNamesMapping().keys():
            assert level in serr.decode()

    def test_log_time(self, caplog):
        """
          Does the `logged` decorator <time> kwarg operate correctly,
          and does this coexist with the <level> positional arg?
        """
        dr = DummyLoggingReader()

        # Two messages should be emitted, one each before and after call
        with caplog.at_level(logging.DEBUG, logger=config.PROGNAME):
            dr.time_log_meth()
        assert len(caplog.records) == 2
        assert caplog.records[0].msg.endswith("start")
        assert caplog.records[1].msg.endswith("end")

        # Two further messages should be emitted, one each before and
        # after call, and both having the level specified in decorator
        with caplog.at_level(logging.DEBUG, logger=config.PROGNAME):
            dr.time_level_log_meth()
        assert len(caplog.records) == 4
        assert caplog.records[2].msg.endswith("start")
        assert caplog.records[3].msg.endswith("end")
        assert caplog.records[2].levelname == "ERROR"
        assert caplog.records[3].levelname == "ERROR"
