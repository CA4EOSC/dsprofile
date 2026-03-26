import logging

import pytest

from dsprofile import config


class TestLogging:
    def test_log_config(caplog):
        conf_logger = config.getLogger()
        prog_logger = logging.getLogger(config.PROGNAME)
        assert conf_logger == prog_logger

    def test_instance_log(caplog):
        pass

    def test_log_cli(caplog):
        pass
