import json
import pytest
import responses

from ns1.alerting import UsageAlertsAPI, USAGE_SUBTYPES


@pytest.fixture
def usage_alerts_client():
    from ns1 import NS1
    client = NS1(apiKey="test1")
    client.config["endpoint"] = "https://api.nsone.net"
    return client


@responses.activate
def test_create_usage_alert(usage_alerts_client):
    """Test creating a usage alert"""
    client = usage_alerts_client
    
    # Mock response for create
    responses.add(
        responses.POST,
        "https://api.nsone.net/alerting/v1/alerts",
        json={
            "id": "a1b2c3",
            "name": "Test Alert",
            "type": "account",
            "subtype": "query_usage",
            "data": {"alert_at_percent": 85},
            "notifier_list_ids": ["n1"],
            "zone_names": [],
            "created_at": 1597937213,
            "updated_at": 1597937213
        },
        status=200,
    )
    
    alert = client.alerting().usage.create(
        name="Test Alert",
        subtype="query_usage",
        alert_at_percent=85,
        notifier_list_ids=["n1"]
    )
    
    assert alert["id"] == "a1b2c3"
    assert alert["name"] == "Test Alert"
    assert alert["type"] == "account"
    assert alert["subtype"] == "query_usage"
    assert alert["data"]["alert_at_percent"] == 85
    assert alert["notifier_list_ids"] == ["n1"]


@responses.activate
def test_get_usage_alert(usage_alerts_client):
    """Test retrieving a usage alert"""
    client = usage_alerts_client
    alert_id = "a1b2c3"
    
    # Mock response for get
    responses.add(
        responses.GET,
        f"https://api.nsone.net/alerting/v1/alerts/{alert_id}",
        json={
            "id": alert_id,
            "name": "Test Alert",
            "type": "account",
            "subtype": "query_usage",
            "data": {"alert_at_percent": 85},
            "notifier_list_ids": ["n1"],
            "zone_names": []
        },
        status=200,
    )
    
    alert = client.alerting().usage.get(alert_id)
    
    assert alert["id"] == alert_id
    assert alert["name"] == "Test Alert"
    assert alert["data"]["alert_at_percent"] == 85


@responses.activate
def test_patch_usage_alert(usage_alerts_client):
    """Test patching a usage alert - verify type/subtype are not sent"""
    client = usage_alerts_client
    alert_id = "a1b2c3"
    
    def request_callback(request):
        payload = json.loads(request.body)
        # Verify type and subtype are not in the request
        assert "type" not in payload
        assert "subtype" not in payload
        # Verify data contains the right alert_at_percent
        assert payload["data"]["alert_at_percent"] == 90
        
        resp_body = {
            "id": alert_id,
            "name": "Updated Alert",
            "type": "account",
            "subtype": "query_usage",
            "data": {"alert_at_percent": 90},
            "notifier_list_ids": ["n1"],
            "zone_names": []
        }
        return (200, {}, json.dumps(resp_body))
    
    responses.add_callback(
        responses.PATCH,
        f"https://api.nsone.net/alerting/v1/alerts/{alert_id}",
        callback=request_callback,
        content_type="application/json",
    )
    
    alert = client.alerting().usage.patch(
        alert_id, 
        name="Updated Alert",
        alert_at_percent=90
    )
    
    assert alert["id"] == alert_id
    assert alert["name"] == "Updated Alert"
    assert alert["data"]["alert_at_percent"] == 90


@responses.activate
def test_delete_usage_alert(usage_alerts_client):
    """Test deleting a usage alert"""
    client = usage_alerts_client
    alert_id = "a1b2c3"
    
    responses.add(
        responses.DELETE,
        f"https://api.nsone.net/alerting/v1/alerts/{alert_id}",
        status=204,
    )
    
    client.alerting().usage.delete(alert_id)
    
    # If we got here without exception, the test passes


@responses.activate
def test_list_usage_alerts(usage_alerts_client):
    """Test listing usage alerts with pagination params"""
    client = usage_alerts_client
    
    responses.add(
        responses.GET,
        "https://api.nsone.net/alerting/v1/alerts",
        json={
            "limit": 1,
            "next": "next_token",
            "total_results": 2,
            "results": [
                {
                    "id": "a1",
                    "name": "Alert 1",
                    "type": "account",
                    "subtype": "query_usage",
                    "data": {"alert_at_percent": 80}
                }
            ]
        },
        status=200,
        match=[
            responses.matchers.query_param_matcher({
                "limit": "1",
                "order_descending": "true"
            })
        ]
    )
    
    response = client.alerting().usage.list(
        limit=1,
        order_descending=True
    )
    
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
        client.alerting().usage.create(
            name="Test Alert",
            subtype="query_usage",
            alert_at_percent=0
        )
    assert "alert_at_percent must be int in 1..100" in str(excinfo.value)
    
    # Test above maximum
    with pytest.raises(ValueError) as excinfo:
        client.alerting().usage.create(
            name="Test Alert",
            subtype="query_usage",
            alert_at_percent=101
        )
    assert "alert_at_percent must be int in 1..100" in str(excinfo.value)
    
    # Test same validation in patch
    with pytest.raises(ValueError) as excinfo:
        client.alerting().usage.patch(
            "a1",
            alert_at_percent=101
        )
    assert "alert_at_percent must be int in 1..100" in str(excinfo.value)


def test_validation_subtype(usage_alerts_client):
    """Test validation of subtype values"""
    client = usage_alerts_client
    
    # Verify all defined subtypes are accepted
    for subtype in USAGE_SUBTYPES:
        try:
            # Just validate, don't make an actual request
            client.alerting().usage._c = None  # This will cause an error if validation passes
            with pytest.raises(AttributeError):
                client.alerting().usage.create(
                    name="Test Alert", 
                    subtype=subtype, 
                    alert_at_percent=85
                )
        except ValueError:
            pytest.fail(f"Valid subtype '{subtype}' was rejected")
    
    # Test invalid subtype
    with pytest.raises(ValueError) as excinfo:
        client.alerting().usage.create(
            name="Test Alert",
            subtype="invalid_subtype",
            alert_at_percent=85
        )
    assert "invalid subtype" in str(excinfo.value)


@responses.activate
def test_404_error_handling(usage_alerts_client):
    """Test proper error handling for 404 responses"""
    client = usage_alerts_client
    alert_id = "nonexistent"
    
    # Mock 404 response with error message
    responses.add(
        responses.GET,
        f"https://api.nsone.net/alerting/v1/alerts/{alert_id}",
        json={"message": "alert not found"},
        status=404,
    )
    
    # This should raise an exception through the REST transport
    with pytest.raises(Exception) as excinfo:
        client.alerting().usage.get(alert_id)
    
    # Verify error contains the message from the server
    assert "alert not found" in str(excinfo.value)
