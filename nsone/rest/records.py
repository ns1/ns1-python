#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.

from . import resource


class Records(resource.BaseResource):

    ROOT = 'zones'

    INT_FIELDS = ['ttl']
    BOOL_FIELDS = ['use_csubnet']
    PASSTHRU_FIELDS = ['feed', 'networks', 'meta', 'regions']

    # answers must be:
    #  1) a single string
    #     we coerce to a single answer with no other fields e.g. meta
    #  2) a list of single strings
    #     we coerce to several answers with no other fields e.g. meta
    #  3) a list of lists
    #     we have as many answers as are in the outer list, and the
    #     answers themselves are used verbatim from the inner list (e.g. may
    #     have MX style [10, '1.1.1.1]), but no other fields e.g. meta
    #     you must use this form for MX records, and if there is only one
    #     answer it still must be wrapped in an outer list
    #  4) a list of dicts
    #     we assume the full rest model and pass it in unchanged. must use this
    #     form for any advanced record config like meta data or data feeds
    def _getAnswersForBody(self, answers):
        realAnswers = []
        # simplest: they specify a single string ip
        if isinstance(answers, str):
            answers = [answers]
        # otherwise, we need a list
        elif not isinstance(answers, list):
            raise Exception('invalid answers format (must be str or list)')
        # at this point we have a list. loop through and build out the answer
        # entries depending on contents
        for a in answers:
            if isinstance(a, str):
                realAnswers.append({'answer': [a]})
            elif isinstance(a, list):
                realAnswers.append({'answer': a})
            elif isinstance(a, dict):
                realAnswers.append(a)
            else:
                raise Exception('invalid answers format: list must contain '
                                'only str, list, or dict')
        return realAnswers

    def _getFiltersForBody(self, filters):
        realFilters = []
        if type(filters) is not dict:
            raise Exception('filter argument must be dict of filter '
                            'name/config pairs')
        for f in filters:
            realFilters.append({'filter': f, 'config': filters[f]})
        return realFilters

    def _buildBody(self, zone, domain, type, **kwargs):
        body = {}
        body['zone'] = zone
        body['domain'] = domain
        body['type'] = type
        if 'filters' in kwargs:
            body['filters'] = self._getFiltersForBody(kwargs['filters'])
        if 'answers' in kwargs:
            body['answers'] = self._getAnswersForBody(kwargs['answers'])
        self._buildStdBody(body, kwargs)
        return body

    def create(self, zone, domain, type,
               callback=None, errback=None, **kwargs):
        body = self._buildBody(zone, domain, type, **kwargs)
        return self._make_request('PUT',
                                  '%s/%s/%s/%s' % (self.ROOT,
                                                   zone,
                                                   domain,
                                                   type.upper()),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def update(self, zone, domain, type,
               callback=None, errback=None, **kwargs):
        body = self._buildBody(zone, domain, type, **kwargs)
        return self._make_request('POST',
                                  '%s/%s/%s/%s' % (self.ROOT,
                                                   zone,
                                                   domain,
                                                   type.upper()),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete(self, zone, domain, type, callback=None, errback=None):
        return self._make_request('DELETE', '%s/%s/%s/%s' %
                                  (self.ROOT,
                                   zone,
                                   domain,
                                   type.upper()),
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, zone, domain, type, callback=None, errback=None):
        return self._make_request('GET', '%s/%s/%s/%s' %
                                  (self.ROOT,
                                   zone,
                                   domain,
                                   type.upper()),
                                  callback=callback,
                                  errback=errback)
