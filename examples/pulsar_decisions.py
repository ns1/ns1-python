#!/usr/bin/env python
#
# Copyright (c) 2014, 2025 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
"""
Example usage of Pulsar Decisions API endpoints.
This example demonstrates how to query Pulsar decision analytics data
using the ns1_python library.
"""
from ns1 import NS1
import time

# NS1 will use config in ~/.nsone by default
api = NS1()

# to specify an apikey here instead, use:

# from ns1 import Config
# config = Config()
# config.createFromAPIKey('<<CLEARTEXT API KEY>>')
# api = NS1(config=config)

# Get current timestamp and 1 hour ago for time-based queries
end_time = int(time.time())
start_time = end_time - 3600  # 1 hour ago


def main():
    """
    Demonstrate various Pulsar Decisions API endpoints.
    """
    print("=" * 60)
    print("Pulsar Decisions API Examples")
    print("=" * 60)

    ############################
    # GET DECISIONS DATA #
    ############################
    print("\n1. Getting decisions data...")
    try:
        decisions = api.pulsardecisions().get_decisions(
            start=start_time, end=end_time, period="1h"
        )
        print(f"   Total decisions: {decisions.get('total', 0)}")
        print(f"   Number of graphs: {len(decisions.get('graphs', []))}")
    except Exception as e:
        print(f"   Error: {e}")

    ############################
    # GET REGIONAL GRAPH DATA #
    ############################
    print("\n2. Getting regional graph data...")
    try:
        region_data = api.pulsardecisions().get_decisions_graph_region(
            start=start_time, end=end_time
        )
        print(f"   Regions found: {len(region_data.get('data', []))}")
        for region in region_data.get("data", [])[:3]:  # Show first 3
            print(
                f"   - {region.get('region')}: {len(region.get('counts', []))} job counts"
            )
    except Exception as e:
        print(f"   Error: {e}")

    ##############################
    # GET TIME-SERIES GRAPH DATA #
    ##############################
    print("\n3. Getting time-series graph data...")
    try:
        time_data = api.pulsardecisions().get_decisions_graph_time(
            start=start_time, end=end_time, period="5m"
        )
        print(f"   Time points: {len(time_data.get('data', []))}")
        if time_data.get("data"):
            first_point = time_data["data"][0]
            print(f"   First timestamp: {first_point.get('timestamp')}")
            print(
                f"   Job counts at first point: {len(first_point.get('counts', []))}"
            )
    except Exception as e:
        print(f"   Error: {e}")

    ##############################
    # GET AREA-BASED DECISIONS #
    ##############################
    print("\n4. Getting area-based decisions...")
    try:
        area_data = api.pulsardecisions().get_decisions_area(
            start=start_time, end=end_time, area="US"
        )
        print(f"   Areas found: {len(area_data.get('areas', []))}")
        for area in area_data.get("areas", [])[:3]:  # Show first 3
            print(
                f"   - {area.get('area_name')}: {area.get('count')} decisions"
            )
    except Exception as e:
        print(f"   Error: {e}")

    ##############################
    # GET ASN-BASED DECISIONS #
    ##############################
    print("\n5. Getting ASN-based decisions...")
    try:
        asn_data = api.pulsardecisions().get_decisions_asn(
            start=start_time, end=end_time
        )
        print(f"   ASNs found: {len(asn_data.get('data', []))}")
        for asn in asn_data.get("data", [])[:3]:  # Show first 3
            print(
                f"   - ASN {asn.get('asn')}: {asn.get('count')} decisions "
                f"({asn.get('traffic_distribution', 0)*100:.1f}% of traffic)"
            )
    except Exception as e:
        print(f"   Error: {e}")

    ##############################
    # GET RESULTS OVER TIME #
    ##############################
    print("\n6. Getting results over time...")
    try:
        results_time = api.pulsardecisions().get_decisions_results_time(
            start=start_time,
            end=end_time,
            job="your-job-id",  # Replace with actual job ID
        )
        print(f"   Time points: {len(results_time.get('data', []))}")
        if results_time.get("data"):
            first_point = results_time["data"][0]
            print(
                f"   Results at first point: {len(first_point.get('results', []))}"
            )
    except Exception as e:
        print(f"   Error: {e}")

    ##############################
    # GET RESULTS BY AREA #
    ##############################
    print("\n7. Getting results by area...")
    try:
        results_area = api.pulsardecisions().get_decisions_results_area(
            start=start_time, end=end_time
        )
        print(f"   Areas found: {len(results_area.get('area', []))}")
        for area in results_area.get("area", [])[:3]:  # Show first 3
            print(
                f"   - {area.get('area')}: {area.get('decision_count')} decisions, "
                f"{len(area.get('results', []))} unique results"
            )
    except Exception as e:
        print(f"   Error: {e}")

    ##############################
    # GET FILTER DATA OVER TIME #
    ##############################
    print("\n8. Getting filter data over time...")
    try:
        filters_time = api.pulsardecisions().get_filters_time(
            start=start_time, end=end_time
        )
        print(f"   Time points: {len(filters_time.get('filters', []))}")
        if filters_time.get("filters"):
            first_point = filters_time["filters"][0]
            print(
                f"   Filters at first point: {len(first_point.get('filters', {}))}"
            )
    except Exception as e:
        print(f"   Error: {e}")

    ###################################
    # GET CUSTOMER-SPECIFIC DECISIONS #
    ###################################
    print("\n9. Getting customer-specific decisions...")
    try:
        customer_id = "your-customer-id"  # Replace with actual customer ID
        customer_data = api.pulsardecisions().get_decision_customer(
            customer_id, start=start_time, end=end_time
        )
        print(f"   Data points: {len(customer_data.get('data', []))}")
        if customer_data.get("data"):
            total = sum(
                point.get("total", 0) for point in customer_data["data"]
            )
            print(f"   Total decisions: {total}")
    except Exception as e:
        print(f"   Error: {e}")

    ###################################
    # GET RECORD-SPECIFIC DECISIONS #
    ###################################
    print("\n10. Getting record-specific decisions...")
    try:
        customer_id = "your-customer-id"  # Replace with actual customer ID
        domain = "example.com"
        rec_type = "A"
        record_data = api.pulsardecisions().get_decision_record(
            customer_id, domain, rec_type, start=start_time, end=end_time
        )
        print(f"   Data points: {len(record_data.get('data', []))}")
        if record_data.get("data"):
            total = sum(point.get("total", 0) for point in record_data["data"])
            print(f"   Total decisions for {domain}/{rec_type}: {total}")
    except Exception as e:
        print(f"   Error: {e}")

    ####################################
    # GET TOTAL DECISIONS FOR CUSTOMER #
    ####################################
    print("\n11. Getting total decisions for customer...")
    try:
        customer_id = "your-customer-id"  # Replace with actual customer ID
        total_data = api.pulsardecisions().get_decision_total(
            customer_id, start=start_time, end=end_time
        )
        print(f"   Total decisions: {total_data.get('total', 0)}")
    except Exception as e:
        print(f"   Error: {e}")

    ################################
    # GET DECISIONS BY RECORD #
    ################################
    print("\n12. Getting decisions by record...")
    try:
        records_data = api.pulsardecisions().get_decisions_records(
            start=start_time, end=end_time
        )
        print(f"   Total decisions: {records_data.get('total', 0)}")
        print(f"   Number of records: {len(records_data.get('records', {}))}")
        for record_key, record_info in list(
            records_data.get("records", {}).items()
        )[:3]:
            print(
                f"   - {record_key}: {record_info.get('count')} decisions "
                f"({record_info.get('percentage_of_total', 0):.1f}%)"
            )
    except Exception as e:
        print(f"   Error: {e}")

    ##############################
    # GET RESULTS BY RECORD #
    ##############################
    print("\n13. Getting results by record...")
    try:
        results_record = api.pulsardecisions().get_decisions_results_record(
            start=start_time, end=end_time
        )
        print(f"   Number of records: {len(results_record.get('record', {}))}")
        for record_key, record_info in list(
            results_record.get("record", {}).items()
        )[:3]:
            print(
                f"   - {record_key}: {record_info.get('decision_count')} decisions, "
                f"{len(record_info.get('results', {}))} unique results"
            )
    except Exception as e:
        print(f"   Error: {e}")

    ##################################
    # QUERYING WITH MULTIPLE FILTERS #
    ##################################
    print("\n14. Querying with multiple filters...")
    try:
        filtered_data = api.pulsardecisions().get_decisions(
            start=start_time,
            end=end_time,
            period="1h",
            area="US",
            job="your-job-id",  # Replace with actual job ID
            agg="sum",
        )
        print(
            f"   Total decisions (filtered): {filtered_data.get('total', 0)}"
        )
    except Exception as e:
        print(f"   Error: {e}")

    ##################################
    # QUERYING WITH MULTIPLE JOBS #
    ##################################
    print("\n15. Querying with multiple jobs...")
    try:
        multi_job_data = api.pulsardecisions().get_decisions(
            start=start_time,
            end=end_time,
            jobs=["job1", "job2", "job3"],  # Replace with actual job IDs
        )
        print(
            f"   Total decisions (multi-job): {multi_job_data.get('total', 0)}"
        )
    except Exception as e:
        print(f"   Error: {e}")

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
