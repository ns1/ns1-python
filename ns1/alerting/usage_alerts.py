from typing import List, Optional, Dict, Any

USAGE_SUBTYPES = {
    "query_usage",
    "record_usage",
    "china_query_usage",
    "rum_decision_usage",
    "filter_chain_usage",
    "monitor_usage",
}


def _validate(name: str, subtype: str, alert_at_percent: int) -> None:
    if not name:
        raise ValueError("name required")
    if subtype not in USAGE_SUBTYPES:
        raise ValueError("invalid subtype")
    if not isinstance(alert_at_percent, int) or not (
        1 <= alert_at_percent <= 100
    ):
        raise ValueError("data.alert_at_percent must be int in 1..100")


class UsageAlertsAPI:
    """
    Account-scoped usage alerts. Triggers when usage ≥ alert_at_percent.

    Server rules:
    - Always type='account'
    - data.alert_at_percent must be in 1..100
    - PATCH must not include type/subtype
    - zone_names/notifier_list_ids may be empty ([])
    - Server ignores datafeed notifiers for usage alerts
    """

    def __init__(self, client) -> None:
        self._c = client

    def create(
        self,
        *,
        name: str,
        subtype: str,
        alert_at_percent: int,
        notifier_list_ids: Optional[List[str]] = None,
        zone_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        _validate(name, subtype, alert_at_percent)
        body = {
            "name": name,
            "type": "account",
            "subtype": subtype,
            "data": {"alert_at_percent": int(alert_at_percent)},
            "notifier_list_ids": notifier_list_ids or [],
            "zone_names": zone_names or [],
        }
        return self._c._post("/alerting/v1/alerts", json=body)

    def get(self, alert_id: str) -> Dict[str, Any]:
        return self._c._get(f"/alerting/v1/alerts/{alert_id}")

    def patch(
        self,
        alert_id: str,
        *,
        name: Optional[str] = None,
        alert_at_percent: Optional[int] = None,
        notifier_list_ids: Optional[List[str]] = None,
        zone_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        patch: Dict[str, Any] = {}
        if name is not None:
            patch["name"] = name
        if alert_at_percent is not None:
            if not isinstance(alert_at_percent, int) or not (
                1 <= alert_at_percent <= 100
            ):
                raise ValueError("data.alert_at_percent must be int in 1..100")
            patch["data"] = {"alert_at_percent": int(alert_at_percent)}
        if notifier_list_ids is not None:
            patch["notifier_list_ids"] = notifier_list_ids
        if zone_names is not None:
            patch["zone_names"] = zone_names
        return self._c._patch(f"/alerting/v1/alerts/{alert_id}", json=patch)

    def delete(self, alert_id: str) -> None:
        self._c._delete(f"/alerting/v1/alerts/{alert_id}")

    def list(
        self,
        *,
        limit: int = 50,
        next: Optional[str] = None,
        order_descending: bool = False,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"limit": limit}
        if next:
            params["next"] = next
        if order_descending:
            params["order_descending"] = "true"
        return self._c._get("/alerting/v1/alerts", params=params)
