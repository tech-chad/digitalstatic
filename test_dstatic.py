""" Test file for dstatic.py script. """

import pytest
from hecate import Runner

import dstatic

cmd = ["python3", "dstatic.py"]


@pytest.mark.parametrize("test_values, expected_results", [
    (0, 0), (1, 0.01), (2, 0.03), (3, 0.06), (4, 0.1),
    (5, 0.15), (6, 0.21), (7, 0.28), (8, 0.36), (9, 0.45)
])
def test_convert_delay_number_to_delay_time(test_values, expected_results):
    result = dstatic.convert_delay_number_to_delay_time(test_values)
    assert result == expected_results


@pytest.mark.parametrize("test_key", ["q", "Q"])
def test_dstatic_exit(test_key):
    """ Tests dstatic.py will exit on q or Q"""
    with Runner(*cmd) as h:
        h.await_text("1")
        h.write(test_key)
        h.press("Enter")
        h.await_exit()

