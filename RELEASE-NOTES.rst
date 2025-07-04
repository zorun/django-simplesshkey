=====================================
Release Notes for django-simplesshkey
=====================================

2.2.0 (2025-06-30)
------------------

* Increase maximum length of SSH key type
* Add support for Django 5.0, 5.1, 5.2
* Add support for Python 3.12, 3.13
* Stop automated testing against obsolete Django versions (< 4.2)

2.1.0 (2023-03-07)
------------------

* Add support for Django 4.0, 4.1, 4.2
* Add CI with linter and tests
* Remove unused setting ``SSHKEY_AUTHORIZED_KEYS_OPTIONS`` (leftover from fork)

2.0.0 (2022-11-01)
------------------

* Add support for Django 3.2
* Drop support for Django < 3.0

1.1.0 (2018-03-25)
------------------

* Add a new field "keytype" (e.g. "ssh-rsa").

1.0.3 (2018-01-08)
------------------

* Add compatibility with Django 2.0

1.0.2 (2017-06-30)
------------------

* Ensure consistent unicode behaviour between python2 and python3.
* Minor admin improvement.

1.0.1 (2017-06-15)
------------------

* Don't crash when parsing malformed SSH key.

1.0.0 (2017-06-12)
------------------

* Remove integration with OpenSSH server: key lookup, scripts, etc.
* Stop sending emails when SSH keys are added or modified.  It's much
  more flexible to do this directly in the application that uses
  django-simplesshkey, using signals.
* Impose less constraints on the SSH keys: allow duplicate keys, keys without name...
* Allow to subclass the UserKey model: can be useful to override some fields.

0.0.0 (2017-06-11)
------------------

* First release of django-simplesshkey fork.  This release is mostly there to help
  migration from django-sshkey, see `README.upgrading.rst`.
* Support Django up to version 1.11.
* Allow to use a custom user model (settings.AUTH_USER_MODEL) instead of hard-coding
  the default Django user model.


===============================
Release Notes for django-sshkey
===============================

2.5.0 (2016-06-16)
------------------

Migration label: 0002

* Stop testing against Django 1.4 through 1.7.
* Start testing against Django 1.9.
* Support for Python 3.3 and 3.4 (issue #6).
* Support OpenSSH 6.8+ MD5 and SHA256 fingerprints (issue #5). Also makes
  django-sshkey compatible with fingerprints of unpatched OpenSSH 6.9+
  ``AuthorizedKeysCommand`` (issue #3). Add ``SSHKEY_DEFAULT_HASH`` setting.
* Add ``import_sshkey`` and ``normalize_sshkeys`` management commands.
* Code formatting cleanup.

2.4.0 (2015-09-21)
------------------

* Support Django 1.4 through Django 1.8.
* Discontinued South migrations in favor of Django native migration system.

2.3.2 (2014-09-15)
------------------

* Bug fix #1: entering whitespace for key field results in IndexError
* Make example templates work with Django 1.4+

2.3.1 (2014-07-29)
------------------

* Add support for Django 1.6
* Add missing dependency for pyasn1 (introduced in 2.3.0)
* Add release notes (this file)

2.3.0 (2014-07-07)
------------------

* Schema change (label 0002): add last_used timestamp
* Provide {key_id} in template for SSHKEY_AUTHORIZED_KEYS_OPTIONS so that
  last_used timestamp may be updated
* Add support for RFC4716 and PEM public keys for import and export
* django-sshkey-lookup can now use any method to lookup keys: all, by username,
  by fingerprint, or compatibility mode
* Add ability to send email to user when a key is added to their account
* Add the following settings
    * SSHKEY_ALLOW_EDIT
    * SSHKEY_EMAIL_ADD_KEY
    * SSHKEY_EMAIL_ADD_KEY_SUBJECT
    * SSHKEY_FROM_EMAIL
    * SSHKEY_SEND_HTML_EMAIL
* Remove setting SSHKEY_AUTHORIZED_KEYS_COMMAND (deprecated since 1.0.0)
* Fix up example templates

2.2.0 (2014-03-26)
------------------

* Change license to BSD 3-clause
* Basic compatability with Django > 1.3
* OpenSSH patch removed, refer to their separate projects
* Remove deprecated sshkey_authorized_keys_command management command
* Add the following lookup commands
    * django-sshkey-lookup-all
    * django-sshkey-lookup-by-fingerprint
    * django-sshkey-lookup-by-username

2.1.0 (2014-01-22)
------------------

* lookup.sh and lookup.py deprecated in favor of django-sshkey-lookup and
  django-sshkey-pylookup, respectively
* Install scripts using setuptools

2.0.1 (2013-09-30)
------------------

* Add missing __init__.py

2.0.0 (2013-09-30)
------------------

* Rename sshkey to django_sshkey

1.1.1 (2013-09-03)
------------------

* Include management and migrations directories in setuptools

1.1.0 (2013-08-28)
------------------

* Schema change (label 0001): add created and last_modified timestamps

1.0.1 (2013-08-28)
------------------

* Add copyright info

1.0.0 (2013-08-28)
------------------

First release
