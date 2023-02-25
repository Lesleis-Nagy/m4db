import os
import textwrap

from tempfile import TemporaryDirectory

import pytest

import requests.exceptions

from m4db_database.rest_api.m4db_runner_web.get_model_merrill_script import get_model_merrill_script


######################################################################################################################
# Service to get the executable for a given software.                                                                #
######################################################################################################################


def test_get_model_merrill_script():

    expected_merrill_script =textwrap.dedent(r"""
        Set MaxMeshNumber 1

        ReadMesh 1 geometry.pat

        Set MaxEnergyEvaluations 10000

        ConjugateGradient
        Set ExchangeCalculator 1


        set subdomain 1 magnetite 20.000



        EnergyLog energy


        Minimize
        WriteMagnetization magnetization
        CloseLogfile

        ReportEnergy

        End""").strip()

    with TemporaryDirectory() as tmp_dir:

        os.chdir(tmp_dir)

        result = get_model_merrill_script("1d73da1c-ea5f-4690-a170-4f6eb442d8e2",
                                          "script.merrill")

        with open("script.merrill") as fin:
            merrill_script = fin.read()

        assert merrill_script == expected_merrill_script
