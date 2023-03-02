import os
import textwrap
import unittest
import xmlrunner

from tempfile import TemporaryDirectory

import pytest

import requests.exceptions

from m4db_database.rest_api.m4db_runner_web.get_model_merrill_script import get_model_merrill_script


######################################################################################################################
# Service to get the executable for a given software.                                                                #
######################################################################################################################

class TestGetModelMerrillScript(unittest.TestCase):

    def test_get_model_merrill_script(self):

        expected_merrill_script = textwrap.dedent(r"""
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

        origin_cwd = os.getcwd()
        with TemporaryDirectory() as tmp_dir:
            print(f"TEMPORARY DIR {tmp_dir}")
            os.chdir(tmp_dir)

            result = get_model_merrill_script("1d73da1c-ea5f-4690-a170-4f6eb442d8e2",
                                              "script.merrill")

            with open("script.merrill") as fin:
                merrill_script = fin.read()

            assert merrill_script == expected_merrill_script
        os.chdir(origin_cwd)


if __name__ == "__main__":
    with open("test-get-model-merrill-script.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
