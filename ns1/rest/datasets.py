from . import resource


class Datasets(resource.BaseResource):
    ROOT = "datasets"

    PASSTHRU_FIELDS = [
        "name",
        "datatype",
        "repeat",
        "timeframe",
        "export_type",
        "recipient_emails",
    ]

    def _buildBody(
        self, name, datatype, repeat, timeframe, export_type, recipient_emails, **kwargs
    ):
        body = {
            "name": name,
            "datatype": datatype,
            "repeat": repeat,
            "timeframe": timeframe,
            "export_type": export_type,
            "recipient_emails": recipient_emails,
        }
        self._buildStdBody(body, kwargs)
        return body

    def create(
        self,
        name,
        datatype,
        repeat,
        timeframe,
        export_type,
        recipient_emails,
        callback=None,
        errback=None,
        **kwargs
    ):
        body = self._buildBody(
            name, datatype, repeat, timeframe, export_type, recipient_emails, **kwargs
        )
        return self._make_request(
            "PUT",
            "%s" % self.ROOT,
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, dtId, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, dtId),
            callback=callback,
            errback=errback,
        )

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s" % self.ROOT,
            callback=callback,
            errback=errback,
        )

    def retrieve(self, dtId, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, dtId),
            callback=callback,
            errback=errback,
        )

    def retrieveReport(self, dtId, rpId, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s/reports/%s" % (self.ROOT, dtId, rpId),
            callback=callback,
            errback=errback,
            skip_json_parsing=True,
        )
