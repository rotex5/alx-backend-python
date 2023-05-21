#!/usr/bin/env python3
""" Module for testing client """

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
from typing import Dict
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

    @patch("client.get_json")
    def test_public_repos(self, mock_json: MagicMock) -> None:
        """
        Test that the list of repos is what you expect from the chosen payload.
        Test that the mocked property and the mocked get_json was called once.
        """
        json_payload = {
            "repos_url": "https://api.github.com/users/google/repos",
            "repos": [
                {
                    "id": 460600860,
                    "name": ".allstar",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                        "node_id": "MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=",
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/.allstar",
                    "created_at": "2022-02-17T20:40:32Z",
                    "updated_at": "2023-04-03T17:58:33Z",
                    "has_issues": True,
                    "forks": 2,
                    "default_branch": "main",
                },
                {
                    "id": 170908616,
                    "name": ".github",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                        "node_id": "MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=",
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/.github",
                    "created_at": "2019-02-15T18:14:38Z",
                    "updated_at": "2023-04-15T18:17:55Z",
                    "has_issues": True,
                    "forks": 194,
                    "default_branch": "master",
                },
            ]
        }
        mock_json.return_value = json_payload["repos"]

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock
                   ) as mock_public:

            mock_public.return_value = json_payload["repos_url"]
            result = GithubOrgClient("google").public_repos()
            check = [".allstar", ".github"]

            self.assertEqual(result, check)

            mock_public.assert_called_once()
            mock_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", False),
        ({"license": {"key": "other_license"}}, "my_license", True)
    ])
    def test_has_license(self,
                         repo: Dict,
                         key: str,
                         expected: bool) -> None:
        """
        Test for GithubOrgClient.has_license
        """
        result = GithubOrgClient.has_license(repo, key)
        self.assertNotEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient class
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Class setup fixtures"""
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]}
        cls.get_patcher = patch('requests.get', **config)
        cls.mock = cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """
        Testing the public_repos method.
        """
        self.assertEqual(GithubOrgClient("google").public_repos(),
                         self.expected_repos)
        self.mock.assert_called()

    def test_public_repos_with_license(self) -> None:
        """
        Testing the public_repos method with a license
        """
        ghbOrg_client = GithubOrgClient("google")
        self.assertEqual(ghbOrg_client.public_repos(), self.expected_repos)
        self.assertEqual(ghbOrg_client.public_repos(license="apache-2.0"),
                         self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Destroys the class fixtures after all test have been ran
        """
        cls.get_patcher.stop()
