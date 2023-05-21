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
    memoize
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


class TestMemoize(unittest.TestCase):
    """
    Testing Memoize function
    """
    def test_memoize(self) -> None:
        """
        Test that when calling a_property twice, the correct result is
        returned but a_method is only called once using assert_called_once
        """
        class TestClass:
            """
            Test Class for wrapping with memoize
            """
            def a_method(self):
                """
                Test method for a_method
                """
                return 42

            @memoize
            def a_property(self):
                """
                Test method for a_property
                """
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()

            mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
