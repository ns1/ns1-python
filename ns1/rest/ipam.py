#
# Copyright (c) 2019 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from . import resource


class Addresses(resource.BaseResource):
    ROOT = 'ipam/address'
    INT_FIELDS = ['network_id', 'address_id', 'root_address_id', ' merged_address_id', 'scope_group_id']
    PASSTHRU_FIELDS = ['prefix', 'type', 'desc', 'kvps', 'tags', 'reserve', 'dhcp_option']
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

    def create_dhcp_option(self, address_id, option_name, option_value, callback=None, errback=None):
        body = {"name": option_name,
                "value": option_value}
        return self._make_request('POST',
                                  '%s/%s/options' % (self.ROOT, address_id),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete_dhcp_option(self, address_id, option_name, callback=None, errback=None):
        params = {"name": option_name}
        return self._make_request('DELETE', '%s/%s/options' % (self.ROOT, address_id),
                                  params=params,
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
    INT_FIELDS = ['scope_group_id', 'valid_lifetime_secs', 'renew_timer_secs', 'rebind_timer_secs', 'service_group_id']
    PASSTHRU_FIELDS = ['dhcp_option', 'dhcpv4', 'dhcpv6', 'name']
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
    ROOT = 'dhcp/scopegroup'

    @classmethod
    def select_from_list(cls, result, address_id):
        for item in result:
            if item.get('address_id') == int(address_id):
                return item
        return None

    def create(self, scopegroup_id, address_id, options, callback=None, errback=None):
        body = {"address_id": address_id,
                "options": options
                }

        def success(result, *args):
            return self.retrieve(scopegroup_id, address_id, callback=callback, errback=errback)

        return self._make_request('POST', '%s/%s/scopes' % (self.ROOT, scopegroup_id),
                                  body=body,
                                  callback=success,
                                  errback=errback)

    def list(self, scopegroup_id, callback=None, errback=None):
        return self._make_request('GET', '%s/%s/scopes' % (self.ROOT, scopegroup_id),
                                  callback=callback,
                                  errback=errback)

    def delete(self, scopegroup_id, address_id, callback=None, errback=None):
        params = {'address_id': address_id}
        return self._make_request('DELETE', '%s/%s/scopes' % (self.ROOT, scopegroup_id),
                                  params=params,
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, scopegroup_id, address_id, callback=None, errback=None):
        result = self.list(scopegroup_id, errback=errback)
        scope = Scopes.select_from_list(result, address_id)

        if callback is not None:
            return callback(scope)
        else:
            return scope


class Reservations(resource.BaseResource):
    ROOT = 'dhcp/scopegroup'
    INT_FIELDS = ['scopegroup_id', 'address_id']
    PASSTHRU_FIELDS = ['mac', 'options']
    BOOL_FIELDS = []

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
        kwargs['options'] = options
        body = self._buildBody(**kwargs)

        def success(result, *args):
            return self.retrieve(scopegroup_id, address_id, callback=callback, errback=errback)

        reservation = self._make_request('POST',
                                         '%s/%s/reservations' % (self.ROOT, scopegroup_id),
                                         body=body,
                                         callback=success,
                                         errback=errback)
        return reservation

    def delete(self, scopegroup_id, address_id, callback=None, errback=None):
        return self._make_request('DELETE',
                                  '%s/%s/reservations?address_id=%s' % (self.ROOT, scopegroup_id, address_id),
                                  callback=callback,
                                  errback=errback)

    def list(self, scopegroup_id, callback=None, errback=None):
        return self._make_request('GET',
                                  '%s/%s/reservations' % (self.ROOT, scopegroup_id),
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, scopegroup_id, address_id, callback=None, errback=None):
        result = self.list(scopegroup_id, errback=errback)
        reservation = Reservations.select_from_list(result, address_id)

        if callback is not None:
            return callback(reservation)
        else:
            return reservation
