import os
import textwrap
import unittest
import xmlrunner

import pytest

import requests.exceptions

from m4db.rest_api.m4db_runner_web.get_model_run_prerequisites import get_model_run_prerequisites


######################################################################################################################
# Test wrapper API for model prerequisites.                                                                          #
######################################################################################################################

class TestGetModelRunPrerequisites(unittest.TestCase):

    def test_get_model_run_prerequisites(self):
        user = os.getenv("USER", None)

        unique_id = "1d73da1c-ea5f-4690-a170-4f6eb442d8e2"

        expected_dict = {
            "merrill-script": textwrap.dedent(r"""

             Set MaxMeshNumber 1

             ReadMesh 1 geometry.pat

             Set MaxEnergyEvaluations 10000

             ConjugateGradient
             Set ExchangeCalculator 1




             magnetite 20.000 C


             CubicRotation 0.0 0.0 0.0


             EnergyLog energy


             Minimize
             WriteMagnetization magnetization
             CloseLogfile

             ReportEnergy

             End""").strip(),
            "geometry-file-abs-path": f"/data/{user}/geometry/04/c5/e3/62/3c/21/48/5b/89/83/bb/de/33/5d/60/fc/geometry.pat",
            "model-dir-abs-path": f"/data/{user}/model/1d/73/da/1c/ea/5f/46/90/a1/70/4f/6e/b4/42/d8/e2",
            'merrill-executable': f'/home/{user}/Install/merrill/1.8.1/bin/merrill',
            'initial-magnetization-data-zip': None,
            'initial-magnetization-finished': None,
            'initial-magnetization-type': 'random_initial_magnetization'
        }

        result = get_model_run_prerequisites(unique_id)

        assert expected_dict == result

    def test_get_model_run_prerequisites_noexist(self):
        unique_id = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"

        with pytest.raises(requests.exceptions.HTTPError):
            result = get_model_run_prerequisites(unique_id)


if __name__ == "__main__":
    with open("test-get-model-run-prerequisites.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
