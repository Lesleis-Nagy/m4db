import falcon
from falcon import testing
import msgpack
import pytest
import json

from m4db_database.rest.m4db_runner_web.service import app


@pytest.fixture
def client():
    return testing.TestClient(app)


######################################################################################################################
# Service to get the executable for a given software.                                                                #
######################################################################################################################


def test_get_software_executable(client):
    expected_dict = {
        "return": "/home/m4dbdev/Install/merrill/1.8.1/bin/merrill"
    }

    response = client.simulate_get("/get-software-executable/merrill/1.8.1")

    response_doc = response.text

    response_dict = json.loads(response_doc)

    assert expected_dict == response_dict


def test_get_software_executable_noexist(client):

    response = client.simulate_get("/get-software-executable/noexist/noexist")

    assert response.status == falcon.HTTP_404


def test_get_software_executable_software_is_empty(client):
    expected_dict = {
        "return": None
    }

    response = client.simulate_get("/get-software-executable/emptysw/0.1.0")

    response_doc = response.text

    response_dict = json.loads(response_doc)

    assert expected_dict == response_dict
