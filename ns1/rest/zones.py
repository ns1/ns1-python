#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from . import resource


class Zones(resource.BaseResource):
    ROOT = "zones"
    SEARCH_ROOT = "search"

    INT_FIELDS = ["ttl", "retry", "refresh", "expiry", "nx_ttl"]
    PASSTHRU_FIELDS = [
        "primary",
        "secondary",
        "hostmaster",
        "meta",
        "networks",
        "link",
        "primary_master",
        "tags",
        "views",
    ]
    BOOL_FIELDS = ["dnssec"]

    ZONEFILE_FIELDS = [
        "networks",
        "views",
    ]

    def _buildBody(self, zone, **kwargs):
        body = {}
        body["zone"] = zone
        self._buildStdBody(body, kwargs)
        return body

    def import_file(
        self, zone, zoneFile, name=None, callback=None, errback=None, **kwargs
    ):
        files = [("zonefile", (zoneFile, open(zoneFile, "rb"), "text/plain"))]
        params = self._buildImportParams(kwargs, name=name)
        return self._make_request(
            "PUT",
            "import/zonefile/%s" % (zone),
            files=files,
            params=params,
            callback=callback,
            errback=errback,
        )

    # Extra import args are specified as query parameters not fields in a JSON object.
    def _buildImportParams(self, fields, name=None):
        params = {}
        # Arrays of values should be passed as multiple instances of the same
        # parameter but the zonefile API expects parameters containing comma
        # seperated values.
        if fields.get("networks") is not None:
            networksStrs = map(str, fields["networks"])
            networksParam = ",".join(networksStrs)
            params["networks"] = networksParam
        if fields.get("views") is not None:
            viewsParam = ",".join(fields["views"])
            params["views"] = viewsParam
        if name is not None:
            params["name"] = name
        return params

    def create(self, zone, name=None, callback=None, errback=None, **kwargs):
        body = self._buildBody(zone, **kwargs)
        if name is None:
            name = zone
        return self._make_request(
            "PUT",
            "%s/%s" % (self.ROOT, name),
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(self, zone, callback=None, errback=None, **kwargs):
        body = self._buildBody(zone, **kwargs)
        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, zone),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, zone, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, zone),
            callback=callback,
            errback=errback,
        )

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s" % self.ROOT,
            callback=callback,
            errback=errback,
            pagination_handler=zone_list_pagination,
        )

    def retrieve(self, zone, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, zone),
            callback=callback,
            errback=errback,
            pagination_handler=zone_retrieve_pagination,
        )

    def search(
        self,
        query,
        type="all",
        expand=True,
        max=None,
        callback=None,
        errback=None,
    ):
        request = "{}?q={}&type={}&expand={}".format(
            self.SEARCH_ROOT, query, type, str.lower(str(expand))
        )
        if max is not None:
            request += "&max=" + str(max)
        return self._make_request(
            "GET",
            request,
            params={},
            callback=callback,
            errback=errback,
        )

    def list_versions(self, zone, callback=None, errback=None):
        request = "{}/{}/versions".format(self.ROOT, zone)
        return self._make_request(
            "GET",
            request,
            params={},
            callback=callback,
            errback=errback,
        )

    def create_version(self, zone, force=False, callback=None, errback=None):
        request = "{}/{}/versions?force={}".format(
            self.ROOT, zone, str.lower(str(force))
        )
        return self._make_request(
            "PUT",
            request,
            params={},
            callback=callback,
            errback=errback,
        )

    def activate_version(self, zone, version_id, callback=None, errback=None):
        request = "{}/{}/versions/{}/activate".format(
            self.ROOT, zone, str(version_id)
        )
        return self._make_request(
            "POST",
            request,
            params={},
            callback=callback,
            errback=errback,
        )

    def delete_version(self, zone, version_id, callback=None, errback=None):
        request = "{}/{}/versions/{}".format(self.ROOT, zone, str(version_id))
        return self._make_request(
            "DELETE",
            request,
            params={},
            callback=callback,
            errback=errback,
        )


# successive pages just extend the list of zones
def zone_list_pagination(curr_json, next_json):
    curr_json.extend(next_json)
    return curr_json


# successive pages only differ in the "records" list
def zone_retrieve_pagination(curr_json, next_json):
    curr_json["records"].extend(next_json["records"])
    return curr_json
