import os

import pytest

from python_template.utils import get_env_variable


def test_get_not_set_env_variable():
    with pytest.raises(ValueError):
        get_env_variable("NOT_SET_ENV_VAR")


def test_get_set_env_variable():
    os.environ["SET_ENV_VAR"] = "value"
    assert get_env_variable("SET_ENV_VAR") == "value"


def test_debug_log_short_env_variable(caplog):
    os.environ["SHORT_ENV_VAR"] = "medium"
    with caplog.at_level("DEBUG"):
        get_env_variable("SHORT_ENV_VAR")
    assert "Environment variable SHORT_ENV_VAR has value m***" in caplog.text
