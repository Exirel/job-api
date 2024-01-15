=======
Job API
=======

This is a test project, a way to explore France Travail's (former Pole Emploi)
APIs.

It is composed of two parts:

* a set of commands to extract and transform a set of data from France Travail
  (ROME 4.0 dataset)
* a small web interface to browser through this set of data


Requirements
============

Project
-------

This project is made with **Python and the Django framework**. The recommended
way to install it is to create a Python **virtualenv**, then to use the
requirement file::

    (venv) $ python -m pip install -U -r requirements.txt

This will install the necessary dependencies to your Python virtualenv for this
project to run.

.. note::

    This project doesn't use any database, as it exists only for demonstration
    purpose. Using a database (SQL or NOSQL) would mean more setup for a
    data set that is less than 5000 items.

France Travail Credentials
--------------------------

This project uses France Travail's APIs, and as such it requires a set of
application credentials: an application ID and an application secret.

Both can be found by creating an application on `France Travail's portal`__.

.. __: https://pole-emploi.io/


Configuration
=============

To execute the features of this project that use the France Travail APIs, you
need to set two env vars:

* **FRANCE_TRAVAIL_ID**: application ID
* **FRANCE_TRAVAIL_SECRET**: application secret

Run
===

ROME 4.0 Dataset
----------------

To retrieve the ROME 4.0 dataset, run the following command::

    (venv) $ python manage.py rome_extract

This will use the France Travail API to collect data and store them in
``DATA/raw_rome.json``.

Then, you can run the following command to transform this raw data into a
usage JSON file::

    (venv) $ python manage.py rome_transform

This will generate the file ``DATA/rome.json``.

HTTP Server
-----------

With the JSON file available, you can run the web application::

    (venv) $ python manage.py runserver

And go to http://127.0.0.1:8000/ in your browser.
