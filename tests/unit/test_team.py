import ns1.rest.permissions as permissions
import ns1.rest.team
import pytest

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def team_config(config):
    config.loadFromDict(
        {
            "endpoint": "api.nsone.net",
            "default_key": "test1",
            "keys": {
                "test1": {
                    "key": "key-1",
                    "desc": "test key number 1",
                }
            },
        }
    )

    return config


def test_rest_team_list(team_config):
    z = ns1.rest.team.Team(team_config)
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with(
        "GET", "account/teams", callback=None, errback=None
    )


@pytest.mark.parametrize("team_id, url", [("1", "account/teams/1")])
def test_rest_team_retrieve(team_config, team_id, url):
    z = ns1.rest.team.Team(team_config)
    z._make_request = mock.MagicMock()
    z.retrieve(team_id)
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


class TestTeamsCreat:
    @pytest.mark.parametrize("name, url", [("test-team", "account/teams")])
    def test_no_perms_set_uses_default_perms(self, team_config, name, url):
        z = ns1.rest.team.Team(team_config)
        z._make_request = mock.MagicMock()
        z.create(name)
        z._make_request.assert_called_once_with(
            "PUT",
            url,
            callback=None,
            errback=None,
            body={"name": name, "permissions": permissions._default_perms},
        )

    @pytest.mark.parametrize("name, url", [("test-team", "account/teams")])
    def test_manage_jobs_set_to_true(self, team_config, name, url):
        z = ns1.rest.team.Team(team_config)
        z._make_request = mock.MagicMock()

        z.create(name, permissions={"monitoring": {"manage_jobs": True}})

        expected_perms = {
            "monitoring": {
                "manage_jobs": False,
                "create_jobs": True,
                "update_jobs": True,
                "delete_jobs": True,
            }
        }
        z._make_request.assert_called_once_with(
            "PUT",
            url,
            callback=None,
            errback=None,
            body={"name": name, "permissions": expected_perms},
        )


class TestTeamsUpdate:
    @pytest.mark.parametrize(
        "team_id, name, ip_whitelist, perms, url",
        [
            (
                "1",
                "test-team",
                [{"name": "Test Whitelist", "values": ["1.1.1.1"]}],
                {"data": {"push_to_datafeeds": True}},
                "account/teams/1",
            )
        ],
    )
    def test_manage_jobs_not_set(
        self, team_config, team_id, name, ip_whitelist, perms, url
    ):
        z = ns1.rest.team.Team(team_config)
        z._make_request = mock.MagicMock()
        z.update(
            team_id, name=name, ip_whitelist=ip_whitelist, permissions=perms
        )
        z._make_request.assert_called_once_with(
            "POST",
            url,
            callback=None,
            errback=None,
            body={
                "id": team_id,
                "name": name,
                "ip_whitelist": ip_whitelist,
                "permissions": perms,
            },
        )

    @pytest.mark.parametrize(
        "team_id, name, ip_whitelist, perms, url",
        [
            (
                "1",
                "test-team",
                [{"name": "Test Whitelist", "values": ["1.1.1.1"]}],
                {"monitoring": {"manage_jobs": True}},
                "account/teams/1",
            )
        ],
    )
    def test_manage_jobs_set_to_true(
        self, team_config, team_id, name, ip_whitelist, perms, url
    ):
        z = ns1.rest.team.Team(team_config)
        z._make_request = mock.MagicMock()
        z.update(
            team_id, name=name, ip_whitelist=ip_whitelist, permissions=perms
        )
        expected_perms = {
            "monitoring": {
                "manage_jobs": False,
                "create_jobs": True,
                "update_jobs": True,
                "delete_jobs": True,
            }
        }
        z._make_request.assert_called_once_with(
            "POST",
            url,
            callback=None,
            errback=None,
            body={
                "id": team_id,
                "name": name,
                "ip_whitelist": ip_whitelist,
                "permissions": expected_perms,
            },
        )


@pytest.mark.parametrize("team_id, url", [("1", "account/teams/1")])
def test_rest_team_delete(team_config, team_id, url):
    z = ns1.rest.team.Team(team_config)
    z._make_request = mock.MagicMock()
    z.delete(team_id)
    z._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )
