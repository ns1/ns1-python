#
# Copyright (c) 2014, 2025 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import resource

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Decisions(resource.BaseResource):
    ROOT = "pulsar/query"
    PASSTHRU_FIELDS = []

    def _build_query_params(self, **kwargs):
        params = {}
        
        if 'start' in kwargs and kwargs['start']:
            params['start'] = int(kwargs['start'])
        if 'end' in kwargs and kwargs['end']:
            params['end'] = int(kwargs['end'])
        if 'period' in kwargs and kwargs['period']:
            params['period'] = kwargs['period']
        if 'area' in kwargs and kwargs['area']:
            params['area'] = kwargs['area']
        if 'asn' in kwargs and kwargs['asn']:
            params['asn'] = kwargs['asn']
        if 'job' in kwargs and kwargs['job']:
            params['job'] = kwargs['job']
        if 'jobs' in kwargs and kwargs['jobs']:
            params['jobs'] = ','.join(kwargs['jobs'])
        if 'record' in kwargs and kwargs['record']:
            params['record'] = kwargs['record']
        if 'result' in kwargs and kwargs['result']:
            params['result'] = kwargs['result']
        if 'agg' in kwargs and kwargs['agg']:
            params['agg'] = kwargs['agg']
        if 'geo' in kwargs and kwargs['geo']:
            params['geo'] = kwargs['geo']
        if 'zone_id' in kwargs and kwargs['zone_id']:
            params['zone_id'] = kwargs['zone_id']
        if 'customer_id' in kwargs and kwargs['customer_id']:
            params['customer_id'] = int(kwargs['customer_id'])
            
        return params

    def _make_query_url(self, path, **kwargs):
        params = self._build_query_params(**kwargs)
        if params:
            return "%s?%s" % (path, urlencode(params))
        return path

    def get_decisions(self, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decisions", **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decisions_graph_region(self, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decisions/graph/region", **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decisions_graph_time(self, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decisions/graph/time", **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decisions_area(self, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decisions/area", **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decisions_asn(self, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decisions/asn", **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decisions_results_time(self, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decisions/results/time", **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decisions_results_area(self, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decisions/results/area", **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_filters_time(self, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decisions/filters/time", **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decision_customer(self, customer_id, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decision/customer/%s" % customer_id, **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decision_customer_undetermined(self, customer_id, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decision/customer/%s/undetermined" % customer_id, **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decision_record(self, customer_id, domain, rec_type, callback=None, errback=None, **kwargs):
        path = self._make_query_url(
            "decision/customer/%s/record/%s/%s" % (customer_id, domain, rec_type),
            **kwargs
        )
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decision_record_undetermined(self, customer_id, domain, rec_type, callback=None, errback=None, **kwargs):
        path = self._make_query_url(
            "decision/customer/%s/record/%s/%s/undetermined" % (customer_id, domain, rec_type),
            **kwargs
        )
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decision_total(self, customer_id, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decision/customer/%s/total" % customer_id, **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decisions_records(self, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decisions/records", **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )

    def get_decisions_results_record(self, callback=None, errback=None, **kwargs):
        path = self._make_query_url("decisions/results/record", **kwargs)
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, path),
            callback=callback,
            errback=errback
        )
