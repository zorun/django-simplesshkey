Upgrading and Downgrading
=========================

Upgrading from django-sshkey
----------------------------

Unfortunately, the migration system does not easily allow to migrate a model
across application rename.

Instead, you must export data from your database and import it back in
django-simplesshkey.

The procedure below has been tested to upgrade from django-sshkey 2.5.0
to django-simplesshkey 1.0.0, with Django 1.11.

* Export your existing SSH keys:

    ./manage.py dumpdata django_sshkey.userkey --natural-foreign --natural-primary --indent 4 > sshkeys.json

* Adapt the dump for the new model name:

    sed -i -e 's/django_sshkey.userkey/simplesshkey.userkey/' sshkeys.json

* Adapt your code to use django-simplesshkey.  It should be as simple as replacing
  all occurrences of "django_sshkey" by "simplesshkey", but beware of other changes,
  for instance if you were using the "last_used" field.

* Install version 0.0.0 of simplesshkey:

    pip install django-simplesshkey==0.0.0

* Remove "django_sshkey" from INSTALLED_APPS and add "simplesshkey" instead.

* Run the initial migration for "simplesshkey":

    ./manage.py migrate simplesshkey

* Import your data:

    ./manage.py loaddata sshkeys.json

* Install the latest version of simplesshkey:

    pip install --upgrade django-simplesshkey

* Run the remaining migrations:

    ./manage.py migrate simplesshkey

This should be it!
