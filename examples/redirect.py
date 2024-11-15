#
# Copyright (c) 2024 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1 import NS1

# NS1 will use config in ~/.nsone by default
api = NS1()

# to specify an apikey here instead, use:
# api = NS1(apiKey='<<CLEARTEXT API KEY>>')

# to load an alternate configuration file:
# api = NS1(configFile='/etc/ns1/api.json')

# turn on "follow pagination". This will handle paginated responses for
# redirect and certificate list. It's off by default.
config = api.config
config["follow_pagination"] = True

redirects = api.redirects()
certificates = api.redirect_certificates()

##########
# CREATE #
##########

# a redirect can only be created on an existing zone
zone = api.createZone("example.com", nx_ttl=3600)

# the simplest redirect, https://domain/path -> target, will have https_enabled=True
# so it will also create a certificate for the domain
redirect_https = redirects.create(
    domain="source.domain.example.com",
    path="/path",
    target="https://www.ibm.com/products/ns1-connect"
)

# an http redirect, http://domain/path -> target, will not hold any certificate for the domain
redirect_http = redirects.create(
    domain="source.domain.example.com",
    path="/all/*",
    target="http://httpforever.com/",
    https_enabled=False,
)

# requesting the certificate manually so that we can use a wildcard;
# note that this wildcard does not include *.domain.example.com, the previous domain
certificate_wildcard = certificates.create("*.example.com")
redirect_allsettings = redirects.create(
    certificate_id=certificate_wildcard["id"],
    domain="files.example.com",
    path="*.rpm",
    target="https://rpmfind.net/",
    https_enabled=True,
    https_forced=True,
    query_forwarding=False,
    forwarding_mode="all",
    forwarding_type="permanent",
    tags=["test","me"],
)

##########
# SEARCH #
##########

# search; we can also use list() to get all redirects
reds = redirects.searchSource('example.com')
print (reds['total'], len(reds['results']))

certs = certificates.search('example.com')
print (certs['total'], len(certs['results']))

#################
# READ / UPDATE #
#################

# read
redirect_tmp = redirects.retrieve(redirect_allsettings["id"])
print(redirect_tmp)

# update
redirect_tmp = redirects.update(
    redirect_tmp,
    forwarding_type="temporary",
)
print(redirect_tmp)

##########
# DELETE #
##########

# delete redirects
redirects.delete(redirect_https['id'])
redirects.delete(redirect_http['id'])
redirects.delete(redirect_allsettings['id'])

# also revoke certificate;
# note that the domain in redirect_http is the same so the certificate is also the same
certificates.delete(redirect_https["certificate_id"])
certificates.delete(redirect_allsettings["certificate_id"])

api.zones().delete('example.com')
