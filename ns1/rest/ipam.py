#
# Copyright (c) 2019 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from . import resource


class Addresses(resource.BaseResource):
    ROOT = 'ipam/address'
    INT_FIELDS = ['network_id', 'address_id', 'root_address_id', ' merged_address_id', 'scope_group_id']
    PASSTHRU_FIELDS = ['prefix', 'status', 'desc', 'kvps', 'tags', 'reserve']
    BOOL_FIELDS = ['parent']

    def _buildBody(self, **kwargs):
        body = {}
        self._buildStdBody(body, kwargs)
        return body

    def create(self, callback=None, errback=None, parent=True, **kwargs):
        body = self._buildBody(**kwargs)
        params = {'parent': parent}
        return self._make_request('PUT',
                                  self.ROOT,
                                  params=params,
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def update(self, address_id, callback=None, errback=None, parent=True, **kwargs):
        body = self._buildBody(**kwargs)
        params = {'parent': parent}
        return self._make_request('POST',
                                  '%s/%s' % (self.ROOT, address_id),
                                  params=params,
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete(self, address_id, callback=None, errback=None):
        return self._make_request('DELETE', '%s/%s' % (self.ROOT, address_id),
                                  callback=callback,
                                  errback=errback)

    def list(self, callback=None, errback=None):
        return self._make_request('GET', '%s' % self.ROOT,
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, address_id, callback=None, errback=None):
        return self._make_request('GET', '%s/%s' % (self.ROOT, address_id),
                                  callback=callback,
                                  errback=errback)

    def retrieve_children(self, address_id, callback=None, errback=None):
        return self._make_request('GET', '%s/%s/children' % (self.ROOT, address_id),
                                  callback=callback,
                                  errback=errback)

    def retrieve_parent(self, address_id, callback=None, errback=None):
        return self._make_request('GET', '%s/%s/parent' % (self.ROOT, address_id),
                                  callback=callback,
                                  errback=errback)

    def report(self, address_id, callback=None, errback=None):
        return self._make_request('GET', '%s/%s/report' % (self.ROOT, address_id),
                                  callback=callback,
                                  errback=errback)

    def retrieve_dhcp_option(self, address_id, callback=None, errback=None):
        return self._make_request('GET', '%s/%s/options' % (self.ROOT, address_id),
                                  callback=callback,
                                  errback=errback)

    # NYI in API
    # def retrieve_next(self, address_id, callback=None, errback=None):
    #     return self._make_request('GET', '%s/%s/next' % (self.ROOT, address_id),
    #                               callback=callback,
    #                               errback=errback)
    #
    # def retrieve_previous(self, address_id, callback=None, errback=None):
    #     return self._make_request('GET', '%s/%s/previous' % (self.ROOT, address_id),
    #                               callback=callback,
    #                               errback=errback)
    #
    # def retrieve_available(self, address_id, callback=None, errback=None):
    #     return self._make_request('GET', '%s/%s/available' % (self.ROOT, address_id),
    #                               callback=callback,
    #                               errback=errback)
    #
    # def merge(self, callback=None, errback=None, force=True, **kwargs):
    #     body = self._buildBody(**kwargs)
    #     params = {'force': force}
    #     return self._make_request('POST',
    #                               '%s/merge' % self.ROOT,
    #                               params=params,
    #                               body=body,
    #                               callback=callback,
    #                               errback=errback)
    #
    # def split(self, address_id, callback=None, errback=None, **kwargs):
    #     body = self._buildBody(**kwargs)
    #     return self._make_request('POST',
    #                               '%s/%s/split' % (self.ROOT, address_id),
    #                               body=body,
    #                               callback=callback,
    #                               errback=errback)

    def search(self, network_id, prefix, callback=None, errback=None):
        return self._make_request('GET', '%s/search/%s/%s' % (self.ROOT, network_id, prefix),
                                  callback=callback,
                                  errback=errback)


class Networks(resource.BaseResource):
    ROOT = 'ipam/network'
    INT_FIELDS = ['network_id']
    PASSTHRU_FIELDS = ['rt', 'name', 'desc', 'kvps', 'tags']
    BOOL_FIELDS = []

    def _buildBody(self, **kwargs):
        body = {}
        self._buildStdBody(body, kwargs)
        return body

    def create(self, callback=None, errback=None, **kwargs):
        body = self._buildBody(**kwargs)
        return self._make_request('PUT',
                                  self.ROOT,
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def update(self, network_id, callback=None, errback=None, **kwargs):
        body = self._buildBody(**kwargs)
        return self._make_request('POST',
                                  '%s/%s' % (self.ROOT, network_id),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete(self, network_id, callback=None, errback=None):
        return self._make_request('DELETE', '%s/%s' % (self.ROOT, network_id),
                                  callback=callback,
                                  errback=errback)

    def list(self, callback=None, errback=None, expand=True):
        params = {'expand': expand}
        return self._make_request('GET', self.ROOT,
                                  params=params,
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, network_id, callback=None, errback=None, expand=True):
        params = {'expand': expand}
        return self._make_request('GET', '%s/%s' % (self.ROOT, network_id),
                                  params=params,
                                  callback=callback,
                                  errback=errback)

    def report(self, network_id, callback=None, errback=None):
        return self._make_request('GET', '%s/%s/report' % (self.ROOT, network_id),
                                  callback=callback,
                                  errback=errback)

    # def search(self, q=None, callback=None, errback=None):
    # params = {}
    # if q is not None:
    #     params['q'] = q
    # return self._make_request('GET', self.SEARCH_ROOT,
    #                           params=params,
    #                           callback=callback,
    #                           errback=errback)


class Scopegroups(resource.BaseResource):
    ROOT = 'dhcp/scopegroup'
    INT_FIELDS = ['id', 'dhcp_service_id', 'valid_lifetime_secs']
    PASSTHRU_FIELDS = ['dhcpv4', 'dhcpv6', 'name']
    BOOL_FIELDS = ['enabled', 'echo_client_id']

    def _buildBody(self, **kwargs):
        body = {}
        self._buildStdBody(body, kwargs)
        return body

    def create(self, callback=None, errback=None, **kwargs):
        body = self._buildBody(**kwargs)
        return self._make_request('PUT',
                                  self.ROOT,
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def update(self, scope_group_id, callback=None, errback=None, **kwargs):
        body = self._buildBody(**kwargs)
        return self._make_request('POST',
                                  '%s/%s' % (self.ROOT, scope_group_id),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete(self, scopegroup_id, callback=None, errback=None):
        return self._make_request('DELETE', '%s/%s' % (self.ROOT, scopegroup_id),
                                  callback=callback,
                                  errback=errback)

    def list(self, callback=None, errback=None):
        return self._make_request('GET', self.ROOT,
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, scope_group_id, callback=None, errback=None):
        return self._make_request('GET', '%s/%s' % (self.ROOT, scope_group_id),
                                  callback=callback,
                                  errback=errback)


class Scopes(resource.BaseResource):
    ROOT = 'dhcp/scope'

    @classmethod
    def select_from_list(cls, result, scope_id):
        for item in result:
            if item.get('id') == int(scope_id):
                return item
        return None

    def create(self, scopegroup_id, address_id, options, callback=None, errback=None):
        body = {"address_id": address_id,
                "scope_group_id": scopegroup_id,
                "options": options
                }

        return self._make_request('PUT', '%s' % (self.ROOT),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def update(self, scope_id, address_id, options, scopegroup_id=None, callback=None, errback=None):
        body = {"address_id": address_id,
                "options": options
                }
        if scopegroup_id is not None:
            body["scope_group_id"] = scopegroup_id,

        return self._make_request('POST', '%s/%s' % (self.ROOT, scope_id),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def list(self, scopegroup_id, callback=None, errback=None):
        return self._make_request('GET', '%s?scopeGroupId=%d' % (self.ROOT, int(scopegroup_id)),
                                  callback=callback,
                                  errback=errback)

    def delete(self, scope_id, callback=None, errback=None):
        return self._make_request('DELETE', '%s/%s' % (self.ROOT, scope_id),
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, scope_id, callback=None, errback=None):
        return self._make_request('GET', '%s/%d' % (self.ROOT, int(scope_id)),
                                  callback=callback,
                                  errback=errback)


class Leases(resource.BaseResource):
    ROOT = 'dhcp/lease'
    INT_FIELDS = ['scope_group_id', 'scope_id', 'limit', 'offset']
    PASSTHRU_FIELDS = []
    BOOL_FIELDS = []

    def list(self, scope_group_id=None, scope_id=None, limit=None, offset=None, callback=None, errback=None):
        params = {}
        if scope_group_id is not None:
            params['scopeGroupId'] = scope_group_id
        if scope_id is not None:
            params['scopeId'] = scope_id
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        return self._make_request('GET', self.ROOT,
                                  callback=callback,
                                  errback=errback,
                                  params=params)


class Reservations(resource.BaseResource):
    ROOT = 'dhcp/reservation'
    INT_FIELDS = ['scope_group_id', 'address_id']
    PASSTHRU_FIELDS = ['mac', 'options']
    BOOL_FIELDS = ['dhcpv6']

    def _buildBody(self, **kwargs):
        body = {}
        self._buildStdBody(body, kwargs)
        return body

    @classmethod
    def select_from_list(cls, result, address_id):
        for item in result:
            if item.get('address_id') == int(address_id):
                return item
        return None

    def create(self, scopegroup_id, address_id, options, callback=None, errback=None, **kwargs):
        kwargs['address_id'] = address_id
        kwargs['scope_group_id'] = scopegroup_id
        kwargs['options'] = options
        body = self._buildBody(**kwargs)

        reservation = self._make_request('PUT',
                                         self.ROOT,
                                         body=body,
                                         callback=callback,
                                         errback=errback)
        return reservation

    def update(self, reservation_id, options, callback=None, errback=None, **kwargs):
        kwargs['options'] = options
        body = self._buildBody(**kwargs)

        return self._make_request('POST', '%s/%s' % (self.ROOT, reservation_id),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete(self, reservation_id, callback=None, errback=None):
        return self._make_request('DELETE',
                                  '%s/%s' % (self.ROOT, reservation_id),
                                  callback=callback,
                                  errback=errback)

    def list(self, scopegroup_id, callback=None, errback=None):
        return self._make_request('GET',
                                  '%s?scopeGroupId=%d' % (self.ROOT, int(scopegroup_id)),
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, reservation_id, callback=None, errback=None):
        return self._make_request('GET',
                                  '%s/%d' % (self.ROOT, int(reservation_id)),
                                  callback=callback,
                                  errback=errback)
