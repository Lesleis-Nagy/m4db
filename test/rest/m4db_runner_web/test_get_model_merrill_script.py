import unittest
import json
import xmlrunner
import textwrap

from falcon import testing

from m4db_database.rest.m4db_runner_web.service import app


class TestGetModelMerrillScript(unittest.TestCase):

    def setUp(self) -> None:
        # Set up the test falcon service.
        self.client = testing.TestClient(app)

    def test_get_merrill_script(self):

        expected_merrill_script =textwrap.dedent(r"""
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

            End""").strip()

        response = self.client.simulate_get("/get-model-merrill-script/1d73da1c-ea5f-4690-a170-4f6eb442d8e2")

        response_dict = json.loads(response.text)

        merrill_script = response_dict["return"]

        print(merrill_script)

        assert expected_merrill_script == merrill_script


if __name__ == "__main__":
    with open("test-get-model-merrill-script-result.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
