#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import permissions
from . import resource


class Team(resource.BaseResource):
    ROOT = "account/teams"
    PASSTHRU_FIELDS = ["name", "ip_whitelist", "permissions"]

    def create(self, name, callback=None, errback=None, **kwargs):
        body = {"name": name}

        if "permissions" not in kwargs:
            if self._config["ddi"]:
                body["permissions"] = permissions._default_perms_ddi
            else:
                body["permissions"] = permissions._default_perms

        self._buildStdBody(body, kwargs)

        # Replace `manage_jobs` with the new split permissions
        if body["permissions"].get("monitoring", {}).get("manage_jobs", False):
            body["permissions"]["monitoring"]["manage_jobs"] = False
            body["permissions"]["monitoring"]["create_jobs"] = True
            body["permissions"]["monitoring"]["update_jobs"] = True
            body["permissions"]["monitoring"]["delete_jobs"] = True

        return self._make_request(
            "PUT",
            "%s" % (self.ROOT),
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(self, team_id, callback=None, errback=None, **kwargs):
        body = {"id": team_id}
        self._buildStdBody(body, kwargs)

        # Replace `manage_jobs` with the new split permissions
        if body["permissions"].get("monitoring", {}).get("manage_jobs", False):
            body["permissions"]["monitoring"]["manage_jobs"] = False
            body["permissions"]["monitoring"]["create_jobs"] = True
            body["permissions"]["monitoring"]["update_jobs"] = True
            body["permissions"]["monitoring"]["delete_jobs"] = True

        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, team_id),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, team_id, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, team_id),
            callback=callback,
            errback=errback,
        )

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET", "%s" % self.ROOT, callback=callback, errback=errback
        )

    def retrieve(self, team_id, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, team_id),
            callback=callback,
            errback=errback,
        )
