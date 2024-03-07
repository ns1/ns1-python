from . import resource


class Redirects(resource.BaseResource):
    ROOT = "redirect"
    SEARCH_ROOT = "redirect"

    PASSTHRU_FIELDS = [
        "id",
        "certificate_id",
        "domain",
        "path",
        "target",
        "tags",
        "forwarding_mode",
        "forwarding_type",
    ]
    BOOL_FIELDS = ["https_enabled", "https_forced", "query_forwarding"]
    INT_FIELDS = ["last_updated"]

    def _buildBody(self, domain, path, target, **kwargs):
        body = {
            "domain": domain,
            "path": path,
            "target": target,
        }
        self._buildStdBody(body, kwargs)
        return body

    def import_file(self, cfg, cfgFile, callback=None, errback=None, **kwargs):
        files = [("cfgfile", (cfgFile, open(cfgFile, "rb"), "text/plain"))]
        return self._make_request(
            "PUT",
            "%s/importexport" % self.ROOT,
            files=files,
            callback=callback,
            errback=errback,
        )

    def create(
        self, domain, path, target, callback=None, errback=None, **kwargs
    ):
        body = self._buildBody(domain, path, target, **kwargs)
        return self._make_request(
            "PUT",
            "%s" % self.ROOT,
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(self, cfg, callback=None, errback=None, **kwargs):
        self._buildStdBody(cfg, kwargs)
        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, cfg["id"]),
            body=cfg,
            callback=callback,
            errback=errback,
        )

    def delete(self, cfgId, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, cfgId),
            callback=callback,
            errback=errback,
        )

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s" % self.ROOT,
            callback=callback,
            errback=errback,
            pagination_handler=redirect_list_pagination,
        )

    def retrieve(self, cfgId, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, cfgId),
            callback=callback,
            errback=errback,
        )

    def searchSource(
        self,
        query,
        max=None,
        callback=None,
        errback=None,
    ):
        request = "{}?source={}".format(self.SEARCH_ROOT, query)
        if max is not None:
            request += "&limit=" + str(max)
        return self._make_request(
            "GET",
            request,
            params={},
            callback=callback,
            errback=errback,
        )

    def searchTarget(
        self,
        query,
        max=None,
        callback=None,
        errback=None,
    ):
        request = "{}?target={}".format(self.SEARCH_ROOT, query)
        if max is not None:
            request += "&limit=" + str(max)
        return self._make_request(
            "GET",
            request,
            params={},
            callback=callback,
            errback=errback,
        )

    def searchTag(
        self,
        query,
        max=None,
        callback=None,
        errback=None,
    ):
        request = "{}?tag={}".format(self.SEARCH_ROOT, query)
        if max is not None:
            request += "&limit=" + str(max)
        return self._make_request(
            "GET",
            request,
            params={},
            callback=callback,
            errback=errback,
        )


class RedirectCertificates(resource.BaseResource):
    ROOT = "redirect/certificates"
    SEARCH_ROOT = "redirect/certificates"

    PASSTHRU_FIELDS = [
        "id",
        "domain",
        "certificate",
        "errors",
    ]
    BOOL_FIELDS = ["processing"]
    INT_FIELDS = [
        "valid_from",
        "valid_until",
        "last_updated",
    ]

    def _buildBody(self, domain, **kwargs):
        body = {
            "domain": domain,
        }
        self._buildStdBody(body, kwargs)
        return body

    def create(self, domain, callback=None, errback=None, **kwargs):
        body = self._buildBody(domain, **kwargs)
        return self._make_request(
            "PUT",
            "%s" % self.ROOT,
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(self, certId, callback=None, errback=None, **kwargs):
        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, certId),
            callback=callback,
            errback=errback,
        )

    def delete(self, certId, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, certId),
            callback=callback,
            errback=errback,
        )

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s" % self.ROOT,
            callback=callback,
            errback=errback,
            pagination_handler=redirect_list_pagination,
        )

    def retrieve(self, certId, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, certId),
            callback=callback,
            errback=errback,
        )

    def search(
        self,
        query,
        max=None,
        callback=None,
        errback=None,
    ):
        request = "{}?domain={}".format(self.SEARCH_ROOT, query)
        if max is not None:
            request += "&limit=" + str(max)
        return self._make_request(
            "GET",
            request,
            params={},
            callback=callback,
            errback=errback,
        )


# successive pages extend the list and the count
def redirect_list_pagination(curr_json, next_json):
    curr_json["count"] += next_json["count"]
    curr_json["results"].extend(next_json["results"])
    return curr_json
