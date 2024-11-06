# test_main.py
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import json
from main import main


@pytest.fixture(scope="module")
def result():

    sample_csv_data = [
        "testPLO500_100_6_BTN_BB_SRP_Ks7d5d_C_BTN_CHECK.csv",
        "testPLO500_100_6_BTN_BB_SRP_Ks7d5d_C_BTN_RAISE75.csv",
    ]

    result = main(*sample_csv_data)
    return result


def test_csv_parsing(result):

    assert "ROOT" in result


def test_json_output_structure(result):

    assert isinstance(result, dict)
