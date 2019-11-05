## 0.14.0 (unreleased)

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
