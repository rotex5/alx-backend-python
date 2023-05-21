#!/usr/bin/env python3
"""
Module for testing the utils module.
"""
from parameterized import parameterized
import unittest
from typing import (
        Dict,
        Tuple,
        Union
)
from utils import (
    access_nested_map,
)


class TestAccessNestedMap(unittest.TestCase):
    """
    Testing Class for Access Nested Map
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(
            self,
            nested_map: Dict,
            path: Tuple[str],
            expected: Union[Dict, int]
            ) -> None:
        """
        Testing method for access_nested_map
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)
