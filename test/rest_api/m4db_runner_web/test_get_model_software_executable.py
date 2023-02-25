import textwrap

import pytest

import requests.exceptions

from m4db_database.rest_api.m4db_runner_web.get_model_software_executable import get_model_software_executable


######################################################################################################################
# Test wrapper API for software executables.                                                                         #
######################################################################################################################


def test_get_software_executable():

    unique_id = "1d73da1c-ea5f-4690-a170-4f6eb442d8e2"

    expected = "/home/m4dbdev/Install/merrill/1.8.1/bin/merrill"

    result = get_model_software_executable(unique_id)

    assert expected == result


def test_get_model_software_noexist():

    unique_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

    with pytest.raises(requests.exceptions.HTTPError):
        result = get_model_software_executable(unique_id)

