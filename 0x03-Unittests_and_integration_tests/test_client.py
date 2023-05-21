#!/usr/bin/env python3
""" Module for testing client """

from client import GithubOrgClient
from parameterized import parameterized
import unittest
from unittest.mock import MagicMock, patch


class TestGithubOrgClient(unittest.TestCase):
    """
    Testing Github Org Client
    """
    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self,
                 org: str,
                 mock: MagicMock) -> None:
        """
        Testing that GithubOrgClient.org returns expected value
        """
        test_class = GithubOrgClient(org)
        test_class.org()
        mock.assert_called_once_with(
                "https://api.github.com/orgs/{}".format(org))
