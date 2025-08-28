#!/usr/bin/env python3
#
# Example of using the Usage Alerts API
#

import os
import json
from ns1 import NS1
from ns1.config import Config

# Create NS1 client
config = {
    "endpoint": "https://api.nsone.net",
    "default_key": "test1",
    "keys": {
        "test1": {
            "key": os.environ.get("NS1_APIKEY", "test1"),
            "desc": "test key",
        }
    },
}

# Create a config from dictionary and create the client
c = Config()
c.loadFromDict(config)
client = NS1(config=c)

# If no real API key is set, we'll get appropriate errors
# This is just an example to show the usage pattern
if not os.environ.get("NS1_APIKEY"):
    print(
        "Using a mock endpoint - for real usage, set the NS1_APIKEY environment variable"
    )


# Usage Alerts API Examples
def usage_alerts_example():
    print("\n=== Usage Alerts Examples ===\n")

    # List all usage alerts
    print("Listing usage alerts:")
    try:
        alerts = client.alerts().usage.list(limit=10)
        print(f"Total alerts: {alerts.get('total_results', 0)}")
        for i, alert in enumerate(alerts.get("results", [])):
            print(f"  {i+1}. {alert.get('name')} (id: {alert.get('id')})")
    except Exception as e:
        print(f"Error listing alerts: {e}")

    # Create a usage alert
    print("\nCreating a usage alert:")
    try:
        alert = client.alerts().usage.create(
            name="Example query usage alert",
            subtype="query_usage",
            alert_at_percent=85,
            notifier_list_ids=[],
            zone_names=[],
        )
        alert_id = alert["id"]
        print(f"Created alert: {alert['name']} (id: {alert_id})")
        print(f"Alert details: {json.dumps(alert, indent=2)}")
    except Exception as e:
        print(f"Error creating alert: {e}")
        return

    # Update the alert
    print("\nUpdating the alert threshold to 90%:")
    try:
        updated = client.alerts().usage.patch(alert_id, alert_at_percent=90)
        print(f"Updated alert: {updated['name']}")
        print(f"New threshold: {updated['data']['alert_at_percent']}%")
    except Exception as e:
        print(f"Error updating alert: {e}")

    # Get alert details
    print("\nGetting alert details:")
    try:
        details = client.alerts().usage.get(alert_id)
        print(f"Alert details: {json.dumps(details, indent=2)}")
    except Exception as e:
        print(f"Error getting alert: {e}")

    # Delete the alert
    print("\nDeleting the alert:")
    try:
        client.alerts().usage.delete(alert_id)
        print(f"Alert {alert_id} deleted successfully")
    except Exception as e:
        print(f"Error deleting alert: {e}")


# Test validation failures
def test_validation():
    print("\n=== Validation Tests ===\n")

    # Test invalid subtype
    print("Testing invalid subtype:")
    try:
        client.alerts().usage.create(
            name="Test alert", subtype="invalid_subtype", alert_at_percent=85
        )
    except ValueError as e:
        print(f"Validation error (expected): {e}")

    # Test threshold too low
    print("\nTesting threshold too low (0):")
    try:
        client.alerts().usage.create(
            name="Test alert", subtype="query_usage", alert_at_percent=0
        )
    except ValueError as e:
        print(f"Validation error (expected): {e}")

    # Test threshold too high
    print("\nTesting threshold too high (101):")
    try:
        client.alerts().usage.create(
            name="Test alert", subtype="query_usage", alert_at_percent=101
        )
    except ValueError as e:
        print(f"Validation error (expected): {e}")


if __name__ == "__main__":
    print("Usage Alerts API Examples")
    print("-" * 30)
    print(
        "Note: To run against the actual API, set the NS1_APIKEY environment variable"
    )
    print("Otherwise, this will run against a mock API endpoint")

    # Run examples
    usage_alerts_example()
    test_validation()
