import pytest

import requests.exceptions

from m4db_database.rest_api.m4db_runner_web.get_software_executable import get_software_executable


######################################################################################################################
# Service to get the executable for a given software.                                                                #
######################################################################################################################


def test_get_software_executable_api():

    expected = "/home/m4dbdev/Install/merrill/1.8.1/bin/merrill"

    result = get_software_executable("merrill", "1.8.1")

    assert expected == result


def test_get_software_executable_noexist():

    with pytest.raises(requests.exceptions.HTTPError):
        result = get_software_executable("noexist", "version")


def test_get_software_executable_software_is_empty():

    result = get_software_executable("emptysw", "0.1.0")

    assert result is None
