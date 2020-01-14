#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

_default_perms = {
    "data": {
        "push_to_datafeeds": False,
        "manage_datasources": False,
        "manage_datafeeds": False,
    },
    "account": {
        "manage_plan": False,
        "manage_users": False,
        "view_invoices": False,
        "manage_teams": False,
        "manage_payment_methods": False,
        "manage_account_settings": False,
        "manage_apikeys": False,
        "view_activity_log": False,
    },
    "monitoring": {
        "manage_jobs": False,
        "manage_lists": False,
        "view_jobs": False,
    },
    "security": {"manage_global_2fa": False},
    "dns": {
        "zones_allow": [],
        "manage_zones": False,
        "zones_deny": [],
        "view_zones": False,
        "zones_allow_by_default": False,
    },
}

_default_perms_ddi = {
    "data": {
        "push_to_datafeeds": False,
        "manage_datasources": False,
        "manage_datafeeds": False,
    },
    "account": {
        "manage_users": False,
        "manage_teams": False,
        "manage_account_settings": False,
        "manage_apikeys": False,
        "view_activity_log": False,
    },
    "monitoring": {
        "manage_jobs": False,
        "manage_lists": False,
        "view_jobs": False,
    },
    "security": {"manage_global_2fa": False, "manage_active_directory": False},
    "dns": {
        "zones_allow": [],
        "manage_zones": False,
        "zones_deny": [],
        "view_zones": False,
        "zones_allow_by_default": False,
    },
    "dhcp": {"manage_dhcp": False, "view_dhcp": False},
    "ipam": {"manage_ipam": False, "view_ipam": False},
}
