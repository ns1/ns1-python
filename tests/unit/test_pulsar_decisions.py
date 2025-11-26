#
# Copyright (c) 2014, 2025 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import ns1.rest.pulsar_decisions
import pytest

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def pulsar_decisions_config(config):
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


@pytest.mark.parametrize(
    "op, args, method, url, kwargs",
    [
        (
            "get_decisions",
            None,
            "GET",
            "pulsar/query/decisions",
            {"callback": None, "errback": None},
        ),
        (
            "get_decisions",
            [{"start": 1234567890, "end": 1234567900}],
            "GET",
            "pulsar/query/decisions?start=1234567890&end=1234567900",
            {"callback": None, "errback": None},
        ),
        (
            "get_decisions_graph_region",
            None,
            "GET",
            "pulsar/query/decisions/graph/region",
            {"callback": None, "errback": None},
        ),
        (
            "get_decisions_graph_time",
            None,
            "GET",
            "pulsar/query/decisions/graph/time",
            {"callback": None, "errback": None},
        ),
        (
            "get_decisions_area",
            None,
            "GET",
            "pulsar/query/decisions/area",
            {"callback": None, "errback": None},
        ),
        (
            "get_decisions_asn",
            None,
            "GET",
            "pulsar/query/decisions/asn",
            {"callback": None, "errback": None},
        ),
        (
            "get_decisions_results_time",
            None,
            "GET",
            "pulsar/query/decisions/results/time",
            {"callback": None, "errback": None},
        ),
        (
            "get_decisions_results_area",
            None,
            "GET",
            "pulsar/query/decisions/results/area",
            {"callback": None, "errback": None},
        ),
        (
            "get_filters_time",
            None,
            "GET",
            "pulsar/query/decisions/filters/time",
            {"callback": None, "errback": None},
        ),
        (
            "get_decision_customer",
            ["12345"],
            "GET",
            "pulsar/query/decision/customer/12345",
            {"callback": None, "errback": None},
        ),
        (
            "get_decision_customer_undetermined",
            ["12345"],
            "GET",
            "pulsar/query/decision/customer/12345/undetermined",
            {"callback": None, "errback": None},
        ),
        (
            "get_decision_record",
            ["12345", "example.com", "A"],
            "GET",
            "pulsar/query/decision/customer/12345/record/example.com/A",
            {"callback": None, "errback": None},
        ),
        (
            "get_decision_record_undetermined",
            ["12345", "example.com", "A"],
            "GET",
            "pulsar/query/decision/customer/12345/record/example.com/A/undetermined",
            {"callback": None, "errback": None},
        ),
        (
            "get_decision_total",
            ["12345"],
            "GET",
            "pulsar/query/decision/customer/12345/total",
            {"callback": None, "errback": None},
        ),
        (
            "get_decisions_records",
            None,
            "GET",
            "pulsar/query/decisions/records",
            {"callback": None, "errback": None},
        ),
        (
            "get_decisions_results_record",
            None,
            "GET",
            "pulsar/query/decisions/results/record",
            {"callback": None, "errback": None},
        ),
    ],
)
def test_rest_pulsar_decisions(
    pulsar_decisions_config, op, args, method, url, kwargs
):
    """Test Pulsar Decisions REST API endpoints."""
    m = ns1.rest.pulsar_decisions.Decisions(pulsar_decisions_config)
    m._make_request = mock.MagicMock()
    operation = getattr(m, op)
    if args is not None:
        if (
            isinstance(args, list)
            and len(args) == 1
            and isinstance(args[0], dict)
        ):
            # Handle kwargs case
            operation(**args[0])
        else:
            # Handle positional args case
            operation(*args)
    else:
        operation()
    m._make_request.assert_called_once_with(method, url, **kwargs)


def test_rest_pulsar_decisions_build_query_params(pulsar_decisions_config):
    """Test _build_query_params helper method."""
    m = ns1.rest.pulsar_decisions.Decisions(pulsar_decisions_config)

    params = m._build_query_params(
        start=1234567890,
        end=1234567900,
        period="1h",
        area="US",
        asn="15169",
        job="test_job",
        jobs=["job1", "job2"],
        record="example.com",
        result="192.0.2.1",
        agg="sum",
        geo="country",
        zone_id="zone123",
        customer_id=12345,
    )

    assert params["start"] == 1234567890
    assert params["end"] == 1234567900
    assert params["period"] == "1h"
    assert params["area"] == "US"
    assert params["asn"] == "15169"
    assert params["job"] == "test_job"
    assert params["jobs"] == "job1,job2"
    assert params["record"] == "example.com"
    assert params["result"] == "192.0.2.1"
    assert params["agg"] == "sum"
    assert params["geo"] == "country"
    assert params["zone_id"] == "zone123"
    assert params["customer_id"] == 12345
