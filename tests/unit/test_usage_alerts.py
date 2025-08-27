#
# Copyright (c) 2025 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
import pytest

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def usage_alerts_client(config):
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
    from ns1 import NS1

    client = NS1(config=config)
    return client


def test_create_usage_alert(usage_alerts_client):
    """Test creating a usage alert"""
    client = usage_alerts_client

    # Create a mock for the _post method
    client._post = mock.MagicMock()
    client._post.return_value = {
        "id": "a1b2c3",
        "name": "Test Alert",
        "type": "account",
        "subtype": "query_usage",
        "data": {"alert_at_percent": 85},
        "notifier_list_ids": ["n1"],
        "zone_names": [],
        "created_at": 1597937213,
        "updated_at": 1597937213,
    }

    # Get the usage API and directly set its client
    usage_api = client.alerts().usage
    usage_api._c = client
    
    # Make the API call
    alert = usage_api.create(
            name="Test Alert",
            subtype="query_usage",
            alert_at_percent=85,
            notifier_list_ids=["n1"],
        )

    # Verify _post was called with correct arguments
    expected_body = {
        "name": "Test Alert",
        "type": "account",
        "subtype": "query_usage",
        "data": {"alert_at_percent": 85},
        "notifier_list_ids": ["n1"],
        "zone_names": [],
    }
    client._post.assert_called_once_with(
        "/alerting/v1/alerts", json=expected_body
    )

    # Verify result
    assert alert["id"] == "a1b2c3"
    assert alert["name"] == "Test Alert"
    assert alert["type"] == "account"
    assert alert["subtype"] == "query_usage"
    assert alert["data"]["alert_at_percent"] == 85


def test_get_usage_alert(usage_alerts_client):
    """Test retrieving a usage alert"""
    client = usage_alerts_client
    alert_id = "a1b2c3"

    # Create a mock for the _get method
    client._get = mock.MagicMock()
    client._get.return_value = {
        "id": alert_id,
        "name": "Test Alert",
        "type": "account",
        "subtype": "query_usage",
        "data": {"alert_at_percent": 85},
        "notifier_list_ids": ["n1"],
        "zone_names": [],
    }

    # Get the usage API and directly set its client
    usage_api = client.alerts().usage
    usage_api._c = client
    
    # Make the API call
    alert = usage_api.get(alert_id)

    # Verify _get was called with correct URL
    client._get.assert_called_once_with(f"/alerting/v1/alerts/{alert_id}")

    # Verify result
    assert alert["id"] == alert_id
    assert alert["name"] == "Test Alert"
    assert alert["data"]["alert_at_percent"] == 85


def test_patch_usage_alert(usage_alerts_client):
    """Test patching a usage alert - verify type/subtype are not sent"""
    client = usage_alerts_client
    alert_id = "a1b2c3"

    # Create a mock for the _patch method
    client._patch = mock.MagicMock()
    client._patch.return_value = {
        "id": alert_id,
        "name": "Updated Alert",
        "type": "account",
        "subtype": "query_usage",
        "data": {"alert_at_percent": 90},
        "notifier_list_ids": ["n1"],
        "zone_names": [],
    }

    # Get the usage API and directly set its client
    usage_api = client.alerts().usage
    usage_api._c = client
    
    # Make the API call
    alert = usage_api.patch(
        alert_id, name="Updated Alert", alert_at_percent=90
    )

    # Verify _patch was called with correct arguments
    expected_body = {"name": "Updated Alert", "data": {"alert_at_percent": 90}}
    client._patch.assert_called_once_with(
        f"/alerting/v1/alerts/{alert_id}", json=expected_body
    )

    # Verify type/subtype are not in the arguments
    call_args = client._patch.call_args[1]["json"]
    assert "type" not in call_args
    assert "subtype" not in call_args

    # Verify result
    assert alert["id"] == alert_id
    assert alert["name"] == "Updated Alert"
    assert alert["data"]["alert_at_percent"] == 90


def test_delete_usage_alert(usage_alerts_client):
    """Test deleting a usage alert"""
    client = usage_alerts_client
    alert_id = "a1b2c3"

    # Create a mock for the _delete method
    client._delete = mock.MagicMock()

    # Get the usage API and directly set its client
    usage_api = client.alerts().usage
    usage_api._c = client
    
    # Make the API call
    usage_api.delete(alert_id)

    # Verify _delete was called with correct URL
    client._delete.assert_called_once_with(f"/alerting/v1/alerts/{alert_id}")


def test_list_usage_alerts(usage_alerts_client):
    """Test listing usage alerts with pagination params"""
    client = usage_alerts_client

    # Create a mock for the _get method
    client._get = mock.MagicMock()
    client._get.return_value = {
        "limit": 1,
        "next": "next_token",
        "total_results": 2,
        "results": [
            {
                "id": "a1",
                "name": "Alert 1",
                "type": "account",
                "subtype": "query_usage",
                "data": {"alert_at_percent": 80},
            }
        ],
    }

    # Get the usage API and directly set its client
    usage_api = client.alerts().usage
    usage_api._c = client
    
    # Make the API call
    response = usage_api.list(limit=1, order_descending=True)

    # Verify _get was called with correct URL and params
    expected_params = {"limit": 1, "order_descending": "true"}
    client._get.assert_called_once_with(
        "/alerting/v1/alerts", params=expected_params
    )

    # Verify result
    assert "results" in response
    assert "next" in response
    assert response["next"] == "next_token"
    assert response["total_results"] == 2
    assert len(response["results"]) == 1
    assert response["results"][0]["id"] == "a1"


def test_validation_threshold_bounds(usage_alerts_client):
    """Test validation of alert_at_percent bounds"""
    client = usage_alerts_client

    # Test below minimum
    with pytest.raises(ValueError) as excinfo:
        client.alerts().usage.create(
            name="Test Alert", subtype="query_usage", alert_at_percent=0
        )
    assert "alert_at_percent must be int in 1..100" in str(excinfo.value)

    # Test above maximum
    with pytest.raises(ValueError) as excinfo:
        client.alerts().usage.create(
            name="Test Alert", subtype="query_usage", alert_at_percent=101
        )
    assert "alert_at_percent must be int in 1..100" in str(excinfo.value)

    # Test same validation in patch
    with pytest.raises(ValueError) as excinfo:
        client.alerts().usage.patch("a1", alert_at_percent=101)
    assert "alert_at_percent must be int in 1..100" in str(excinfo.value)


def test_validation_subtype():
    """Test validation of subtype values"""
    from ns1.alerting import USAGE_SUBTYPES
    from ns1.alerting.usage_alerts import _validate

    # Valid subtypes should pass validation
    for subtype in USAGE_SUBTYPES:
        try:
            _validate("Test Alert", subtype, 85)
        except ValueError:
            pytest.fail(f"Valid subtype '{subtype}' was rejected")

    # Invalid subtype should fail validation
    with pytest.raises(ValueError) as excinfo:
        _validate("Test Alert", "invalid_subtype", 85)
    assert "invalid subtype" in str(excinfo.value)
