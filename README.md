[![Build Status](https://travis-ci.org/ns1/ns1-python.svg?branch=master)](https://travis-ci.org/ns1/ns1-python) [![Docs](https://readthedocs.org/projects/ns1-python/badge/?version=latest)](https://ns1-python.readthedocs.io/en/latest/)

NS1 Python SDK
==============

> This project is in [active development](https://github.com/ns1/community/blob/master/project_status/ACTIVE_DEVELOPMENT.md).

A Python SDK for accessing NS1, the Data Driven DNS platform.

About
=====

This package provides a python SDK for accessing the NS1 DNS platform
and includes both a simple NS1 REST API wrapper as well as a higher level
interface for managing zones, records, data feeds, and more.
It supports synchronous and asynchronous transports.

Python 3.8+ is supported. Automated tests are currently run
against 3.8, 3.9, 3.10, 3.11, 3.12 and 3.13

Installation
============

    $ pip install ns1-python

Dependencies
============

None, but supports different transport backends. Currently supported:

* [requests](http://docs.python-requests.org/en/latest/) (synchronous, the
  default if available)
* urllib (synchronous, the default if requests isn't available)
* [twisted](https://twistedmatrix.com/) (asynchronous, requires 2.7 or 3.5+)

Other transports are easy to add, see
[transport](https://github.com/ns1/ns1-python/tree/master/ns1/rest/transport)

Examples
========

See the [examples directory](https://github.com/ns1/ns1-python/tree/master/examples)

Documentation
=============

If you don't yet have an NS1 account, [signup here (free)](https://ns1.com/signup/)

You'll need an API Key. To create one, login to [the portal](https://my.nsone.net/)
and click on the Account button in the top right. Select Settings & Users, then
add a new API Key at the bottom.

* [Documentation at ReadTheDocs](https://ns1-python.readthedocs.org/en/latest/)
* [NS1 REST API Documentation](https://ns1.com/api/)

Tests
=====

Unit tests use `pytest` (`pip install pytest`). 2.7 also requires `mock` to be
installed (`pip install mock`).

Tests should, of course, run and pass under python 2 and 3. We use tox to
automate test runs and virtualenv setup, see `tox.ini` for config.

Contributions
=============
Pull Requests and issues are welcome. See the
[NS1 Contribution Guidelines](https://github.com/ns1/community) for more
information.

### Editing the docs

You can create or edit NS1-python documentation by downloading the repo onto your machine and using an editor such as VSCode.

### Creating Pull Requests

1. When you're ready to submit your changes, add a descriptive title and comments to summarize the changes made.
2. Select **Create a new branch for this commit and start a pull request**.
3. Check the **Propose file change** button.
4. Scroll down to compare changes with the original document.
5. Select **Create pull request**.

Our CI process will lint and check for formatting issues with `flake8` and
`black`.
It is suggested to run these checks prior to submitting a pull request and fix
any issues:
```
pip install flake8 black
flake8 . --count --show-source --statistics --extend-ignore=E501
black . --check -l 79 --diff
```
