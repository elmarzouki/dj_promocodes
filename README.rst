dj_promocodes
=============

promocodes demo

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy dj_promocodes

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html





Deployment
----------

The following details how to deploy this application.



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html




Run and go
----------
run the app using docker

Docker
^^^^^^
::

  $ docker-compose -f local.yml build
  $ docker-compose -f local.yml up -d

  $ docker-compose -f local.yml run django python manage.py makemigrations
  $ docker-compose -f local.yml run django python manage.py migrate
  $ docker-compose -f local.yml run django python manage.py createsuperuser
  $ firefox http://localhost:8000/admin/


If you need a shell, run: `docker-compose -f local.yml run --rm django python manage.py shell_plus`
To check the logs out, run: `docker-compose -f local.yml logs`


Use Promocodes
--------------

1. Dashboard Example: 
    GET http://0.0.0.0:8000/admin/promocodes/promocode/add/
    GET http://0.0.0.0:8000/admin/promocodes/balance/add/

2. DRF API Example: GET http://0.0.0.0:8000/api/promocodes/promocode/<str:promocode_code>

3. Pay:
  POST http://0.0.0.0:8000/api/promocodes/pay
  `json
    {
      "amount": amount,
      "promocode_code": "promocode_code",
      "user_id": user_id
    }
  `