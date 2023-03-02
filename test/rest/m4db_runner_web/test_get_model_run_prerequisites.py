import os
import unittest
import json
import xmlrunner
import textwrap

import falcon
from falcon import testing

from m4db_database.configuration import read_config_from_environ
from m4db_database.rest.m4db_runner_web.service import app


######################################################################################################################
# Service to get the prerequisites of a model run.                                                                   #
######################################################################################################################

class TestGetModelRunPrerequisites(unittest.TestCase):

    def setUp(self) -> None:
        self.client = testing.TestClient(app)

    def test_get_model_run_prerequisites(self):

        user = os.getenv("USER", None)
        assert user is not None

        config = read_config_from_environ()

        expected_dict = {
            "return": {
                "merrill-script": textwrap.dedent(r"""
                    Set MaxMeshNumber 1

                    ReadMesh 1 geometry.pat

                    Set MaxEnergyEvaluations 10000

                    ConjugateGradient
                    Set ExchangeCalculator 1


                    magnetite 20.000 C

                    EnergyLog energy


                    Minimize
                    WriteMagnetization magnetization
                    CloseLogfile

                    ReportEnergy

                    End""").strip(),
                "geometry-file-abs-path": f"{config.database.file_root}/geometry/04/c5/e3/62/3c/21/48/5b/89/83/bb/de/33/5d/60/fc/geometry.pat",
                "model-dir-abs-path": f"{config.database.file_root}/model/1d/73/da/1c/ea/5f/46/90/a1/70/4f/6e/b4/42/d8/e2",
                'merrill-executable': f'/home/{user}/Install/merrill/1.8.1/bin/merrill',
                'initial-magnetization-data-zip': None,
                'initial-magnetization-finished': None,
                'initial-magnetization-type': 'random_initial_magnetization'
            }
        }

        response = self.client.simulate_get("/get-model-run-prerequisites/1d73da1c-ea5f-4690-a170-4f6eb442d8e2")

        response_dict = json.loads(response.text)

        assert expected_dict["return"]["merrill-script"] == response_dict["return"]["merrill-script"]
        assert expected_dict["return"]["geometry-file-abs-path"] == response_dict["return"]["geometry-file-abs-path"]
        assert expected_dict["return"]["model-dir-abs-path"] == response_dict["return"]["model-dir-abs-path"]
        assert expected_dict["return"]["merrill-executable"] == response_dict["return"]["merrill-executable"]
        assert expected_dict["return"]["initial-magnetization-data-zip"] == response_dict["return"]["initial-magnetization-data-zip"]
        assert expected_dict["return"]["initial-magnetization-finished"] == response_dict["return"]["initial-magnetization-finished"]
        assert expected_dict["return"]["initial-magnetization-type"] == response_dict["return"]["initial-magnetization-type"]

    def test_get_model_run_prerequisites_noexist(self):

        response = self.client.simulate_get("/get-model-run-prerequisites/noexist")

        assert response.status == falcon.HTTP_404


if __name__ == "__main__":
    with open("test-get-model-run-prerequisites.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
