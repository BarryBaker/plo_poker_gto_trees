# test_main.py
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import json
from main import main
from main_utils import parse_csv_name, merge_csvs


@pytest.fixture(scope="module")
def sample_csv_data():
    return [
        "testPLO500_100_6_BTN_BB_SRP_Ks7d5d_C_BTN_CHECK.csv",
        "testPLO500_100_6_BTN_BB_SRP_Ks7d5d_C_BTN_RAISE75.csv",
    ]


@pytest.fixture(scope="module")
def result(sample_csv_data):

    return main(*sample_csv_data)


def test_csv_parsing(result):

    assert "ROOT" in result


def test_json_output_structure(result):

    assert isinstance(result, dict)


def test_parsing():

    assert parse_csv_name(["testPLO500_100_6_BTN_BB_SRP_Ks7d5d_C_BTN_CHECK.csv"]) == (
        "Ks7d5d",
        "C",
        "SRP",
    )


def test_merge_columns(sample_csv_data):

    assert len(merge_csvs(sample_csv_data).columns) == len(sample_csv_data)
