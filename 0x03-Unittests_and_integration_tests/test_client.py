#!/usr/bin/env python3
""" Module for testing client """

from client import GithubOrgClient
from parameterized import parameterized
import unittest
from unittest.mock import (
    MagicMock,
    PropertyMock,
    patch,
)


class TestGithubOrgClient(unittest.TestCase):
    """
    Testing Github Org Client
    """
    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self,
                 org: str,
                 mock: MagicMock) -> None:
        """
        Testing that GithubOrgClient.org returns expected value
        """
        test_client = GithubOrgClient(org)
        test_client.org()
        mock.assert_called_once_with(
                "https://api.github.com/orgs/{}".format(org))

    def test_public_repos_url(self) -> None:
        """
        Testing that _public_repos_url returns expected value
        based on the mocked payload
        """
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock
                   ) as mock:
            payload = {
                    "repos_url": "https://api.github.com/users/abc"}
            mock.return_value = payload
            test_client = GithubOrgClient("abc")
            result = test_client._public_repos_url
            self.assertEqual(result, payload["repos_url"])
