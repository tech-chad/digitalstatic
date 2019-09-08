""" Test file for dstatic.py script. """

import pytest

import dstatic


@pytest.mark.parametrize("test_values, expected_results", [
    (0, 0), (1, 0.01), (2, 0.03), (3, 0.06), (4, 0.1),
    (5, 0.15), (6, 0.21), (7, 0.28), (8, 0.36), (9, 0.45)
])
def test_convert_delay_number_to_delay_time(test_values, expected_results):
    result = dstatic.convert_delay_number_to_delay_time(test_values)
    assert result == expected_results

