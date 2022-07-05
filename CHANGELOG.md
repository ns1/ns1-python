## 0.17.4 (July 5, 2022)
* Fix release tag

## 0.17.3 (June 27, 2022)
ENHANCEMENTS:
* Add support for DHCP objects
* Add ability to set `tags` and `primary_master` for DNS zones
* Add support for DNS Views and ACLs

## 0.17.2 (March 30, 2022)
ENHANCEMENTS:
* Adds support for TSIG

## 0.17.1 (October 27, 2021)
BUG FIXES:
* Fixes a casing issue on a search parameter

## 0.17.0 (October 27, 2021)
ENHANCEMENTS
* Move from deprecated search endpoint to supported search endpoint

## 0.16.1 (September 1, 2021)

ENHANCEMENTS
* Re-use connections with Session objects in RequestsTransport

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
