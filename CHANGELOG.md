## 0.17.0 (Unreleased)

ENHANCEMENTS:

Support for DNS views in API v3.x
* acls, views, tsig endpoints supported
* changes to support zone and record model changes (see below)
* examples added for dns-views and dns-views-compatibility

(POTENTIAL) BREAKING CHANGES:

Some low level changes in the data model may lead to issues, despite efforts
to keep things back compatible:

With support for views in v3.x, zone FQDNs are no longer required to be unique
within the system. The "zone" value for functions and methods, which served as
both the unique identifier in NS1s system and as the zone's FQDN, becomes a
unique identifier that may or may not be identical to the FQDN.

This "zone name" is used in the URL for API calls, and is present on Zone
objects as "name" and as "zone_name" for Records. For compatibility, the "zone"
value on Zones and Records remains the FQDN.

When we need to uniquely identify a zone, it's important to use the zone name
and not the FQDN, if they are different. When creating a zone with a non-FQDN
identifier, the FQDN must be provided. For compatibility, if an FQDN is not
provided, we assume it matches the "zone name". However, this means we cannot
validate intent.

For 2.x, this SDK release should be compatible - the "name" and "fqdn" of the
zone just have to match, and the 2.x API still enforces that they do.

Highlights:

* "zone" arg is generally renamed to "zone_name". This reflects its use as an
  identifier.
* When the zone_name is not the FQDN, rather than change method arguments, we
  look for the FQDN value in kwargs.
* When required, an optional "fqdn" argument is added to methods.
* To help disambiguate error and user intention, we've added some simple
  client-side validation that:
  * fqdn args are not invalid
  * when zone_name == fqdn, they are not invalid

DEPRECATED CONVENIENCES:

For records, the SDK tries to help out if you just pass the domain, or allow
you to omit the zone if you pass a fully-qualified domain. This is error prone
with named zones. Especially in automated code, you should use the full domain,
and not rely on this behavior.

## 0.16.0 (May 18, 2020)

ENHANCEMENTS
* Added tags to ipam/dhcp resources

## 0.15.0 (February 20, 2020)

ENHANCEMENTS

* Support monitoring regions endpoint [#55](https://github.com/ns1/ns1-python/pull/55)
* Support job types endpoint [#55](https://github.com/ns1/ns1-python/pull/55)
* Support for following pagination in the endpoints that have it. Off by
  default to avoid breaking changes. Enable in config by setting
  `follow_pagination` to True. [#56](https://github.com/ns1/ns1-python/pull/56)
* Clarify usage caveats in loadRecord docstring [#58](https://github.com/ns1/ns1-python/pull/58)

## 0.14.0 (February 03, 2020)

ENHANCEMENTS:

* Add REST support for teams, users, and API keys
* various IPAM features added
* support for rate limit "strategies" [#47](https://github.com/ns1/ns1-python/pull/47)
* codebase linted (w/black) and GH action for keeping it that way
* project status added to README

BUG FIXES:

* wrong args passed to reservation.delete [#42](https://github.com/ns1/ns1-python/pull/42)

POTENTIAL BREAKING CHANGES:

* Changes to ipam.Address model for (private DNS) v2.2, v2.1 users should stick
  to the previous SDK version (v0.13.0) [#41](https://github.com/ns1/ns1-python/pull/41)

## 0.13.0 (November 05, 2019)

ENHANCEMENTS:

* Add a helper class for concurrency [#40](https://github.com/ns1/ns1-python/pull/40)
* Add `update` methods to scopes and reservations [#39](https://github.com/ns1/ns1-python/pull/39)

## 0.12.0 (September 04, 2019)

ENHANCEMENTS:

* Add (required) `sourcetype` arg to `source.update`. API requires it, although it cannot be changed. [#38](https://github.com/ns1/ns1-python/pull/38)
* Add lease reporting endpoint [#37](https://github.com/ns1-python/pull/37)

IMPROVEMENTS:

* Add unit tests for data (source) [#38](https://github.com/ns1-python/pull/38)

## 0.11.0 (August 05, 2019)

ENHANCEMENTS:

* Added `use_client_subnet` (alias for `use_csubnet`) parameter to `records` resource [#36](https://github.com/ns1/ns1-python/pull/36).  Thanks to @ignatenkobrain!
* Added `primary` parameter to `zones` resource [#35](https://github.com/ns1/ns1-python/pull/35)

IMPROVEMENTS:

* Allow Scopegroups to be loaded by ID [#33](https://github.com/ns1/ns1-python/pull/33)
