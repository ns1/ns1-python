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
        self,
        name: str,
        datatype: dict,
        repeat: dict,
        timeframe: dict,
        export_type: str,
        recipient_emails: list,
        **kwargs
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
        name: str,
        datatype: dict,
        repeat: dict,
        timeframe: dict,
        export_type: str,
        recipient_emails: list,
        callback=None,
        errback=None,
        **kwargs
    ):
        body = self._buildBody(
            name,
            datatype,
            repeat,
            timeframe,
            export_type,
            recipient_emails,
            **kwargs
        )
        return self._make_request(
            "PUT",
            "%s" % self.ROOT,
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, dtId: str, callback=None, errback=None):
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

    def retrieve(self, dtId: str, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, dtId),
            callback=callback,
            errback=errback,
        )

    def retrieveReport(
        self, dtId: str, rpId: str, callback=None, errback=None
    ):
        return self._make_request(
            "GET",
            "%s/%s/reports/%s" % (self.ROOT, dtId, rpId),
            callback=callback,
            errback=errback,
            skip_json_parsing=True,
        )
