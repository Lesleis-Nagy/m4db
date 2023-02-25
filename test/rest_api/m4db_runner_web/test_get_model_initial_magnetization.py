import os
import textwrap

from tempfile import TemporaryDirectory

import pytest

import requests.exceptions

from m4db_database.rest_api.m4db_runner_web.get_model_initial_magnetization import get_model_initial_magnetization


######################################################################################################################
# Test wrapper API for initial magnetizations.                                                                       #
######################################################################################################################


def test_get_model_initial_magnetization():

    unique_id = "1d73da1c-ea5f-4690-a170-4f6eb442d8e2"

    expected_dict = {
        "type": "random"
    }

    result = get_model_initial_magnetization(unique_id)

    assert expected_dict == result


def test_get_model_initial_magnetization_noexist():

    unique_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

    with pytest.raises(requests.exceptions.HTTPError):
        result = get_model_initial_magnetization(unique_id)

