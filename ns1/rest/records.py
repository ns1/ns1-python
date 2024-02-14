#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
import sys

from . import resource


py_str = str if sys.version_info[0] == 3 else basestring  # noqa: F821


class Records(resource.BaseResource):
    ROOT = "zones"

    INT_FIELDS = ["ttl"]
    BOOL_FIELDS = ["use_client_subnet", "use_csubnet", "override_ttl"]
    PASSTHRU_FIELDS = ["networks", "meta", "regions", "link"]

    # answers must be:
    #  1) a single string
    #     we coerce to a single answer with no other fields e.g. meta
    #  2) an iterable of single strings
    #     we coerce to several answers with no other fields e.g. meta
    #  3) an iterable of iterables
    #     we have as many answers as are in the outer iterable, and the
    #     answers themselves are used verbatim from the inner iterable (e.g. may
    #     have MX style [10, '1.1.1.1']), but no other fields e.g. meta
    #     you must use this form for MX records, and if there is only one
    #     answer it still must be wrapped in an outer iterable
    #  4) an iterable of dicts
    #     we assume the full rest model and pass it in unchanged. must use this
    #     form for any advanced record config like meta data or data feeds
    def _getAnswersForBody(self, answers):
        realAnswers = []
        # simplest: they specify a single string ip

        if isinstance(answers, py_str):
            answers = [answers]
        # otherwise, we need an iterable
        elif not isinstance(answers, Iterable):
            raise Exception("invalid answers format (must be str or iterable)")
        # at this point we have a list. loop through and build out the answer
        # entries depending on contents

        for a in answers:
            if isinstance(a, py_str):
                realAnswers.append({"answer": [a]})
            elif isinstance(a, (list, tuple)):
                realAnswers.append({"answer": a})
            elif isinstance(a, dict):
                realAnswers.append(a)
            else:
                raise Exception(
                    "invalid answers format: list must contain "
                    "only str, list, or dict"
                )

        return realAnswers

    # filters must be a list of dict which can have two forms:
    # 1) simple: each item in list is a dict with a single key and value. the
    #            key is the name of the filter, the value is a dict of config
    #            values (which may be empty {})
    # 2) full: each item in the list is a dict of the full rest model for
    #          filters (documented elsewhere) which is passed through. use this
    #          for enabled/disabled or future fields not supported otherwise
    #
    def _getFiltersForBody(self, filters):
        realFilters = []

        if type(filters) is not list:
            raise Exception("filter argument must be list of dict")

        for f in filters:
            if type(f) is not dict:
                raise Exception("filter items must be dict")

            if "filter" in f:
                # full
                realFilters.append(f)
            else:
                # simple, synthesize
                (fname, fconfig) = f.popitem()
                realFilters.append({"filter": fname, "config": fconfig})

        return realFilters

    def _buildBody(self, zone, domain, type, **kwargs):
        body = {}
        body["zone"] = zone
        body["domain"] = domain
        body["type"] = type.upper()

        if "filters" in kwargs:
            body["filters"] = self._getFiltersForBody(kwargs["filters"])

        if "answers" in kwargs:
            body["answers"] = self._getAnswersForBody(kwargs["answers"])

        self._buildStdBody(body, kwargs)

        if "use_csubnet" in body:
            # key mapping
            body["use_client_subnet"] = body["use_csubnet"]
            del body["use_csubnet"]

        return body

    def create(
        self, zone, domain, type, callback=None, errback=None, **kwargs
    ):
        body = self._buildBody(zone, domain, type, **kwargs)

        return self.create_raw(
            zone,
            domain,
            type,
            body,
            callback=callback,
            errback=errback,
            **kwargs
        )

    def create_raw(
        self, zone, domain, type, body, callback=None, errback=None, **kwargs
    ):
        return self._make_request(
            "PUT",
            "%s/%s/%s/%s" % (self.ROOT, zone, domain, type.upper()),
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(
        self, zone, domain, type, callback=None, errback=None, **kwargs
    ):
        body = self._buildBody(zone, domain, type, **kwargs)

        return self._make_request(
            "POST",
            "%s/%s/%s/%s" % (self.ROOT, zone, domain, type.upper()),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, zone, domain, type, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s/%s/%s" % (self.ROOT, zone, domain, type.upper()),
            callback=callback,
            errback=errback,
        )

    def retrieve(self, zone, domain, type, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s/%s/%s" % (self.ROOT, zone, domain, type.upper()),
            callback=callback,
            errback=errback,
        )
