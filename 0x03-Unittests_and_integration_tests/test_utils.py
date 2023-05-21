#!/usr/bin/env python3
"""
Module for testing the utils module.
"""
from parameterized import parameterized
import unittest
from unittest.mock import patch, Mock
from typing import (
        Dict,
        Tuple,
        Union
)
from utils import (
    access_nested_map,
    get_json,
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

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict,
            path: Tuple[str],
            expected: str):
        """
        Testing KeyError raised based on the respective inputs
        """
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual("'{}'".format(expected), str(e.exception))


class TestGetJson(unittest.TestCase):
    """
    Testing class for Get Json
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict
            ) -> None:
        """
        Testing utils.get_json returns expected output
        """
        mock = Mock()
        mock.json.return_value = test_payload
        with patch('requests.get', return_value=mock):
            self.assertEqual(get_json(test_url), test_payload)
