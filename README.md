staff.sitcon.org
================
SITCON Internal Tracking & Conference Operation Network (Codename Roboconf) for Students' Information Technology CONference (SITCON). The website is used to operate though SITCON's administration process since 2014.

Proposed Functionalities
------------------------
* Document operations
* Issue tracker
* Time control
* Staff management

Requirements
------------
Python package dependency are enlisted in [requirements file](requirements.txt).

You could safely remove these packages if you’re not targeting PostgreSQL databases:

* dj-database-url
* psycopg2

[Compass](compass-style.org) and [Fabric](http://fabfile.org) powers site theming and automating respectively.

Development
-----------
It is recommended to use `virtualenv`.

	cd staff.sitcon.org
	virtualenv venv
	. venv/bin/activate # if you use bash

Install dependencies.

	pip install -r requirements-dev.txt

Set debug

	export DEBUG=1 # bash

Load database schema and initial data

	python manage.py syncdb
	python manage.py loaddata */fixtures/*.json

_Note: currently there are problems with loaddata on `master` branch, see commit 5d8436149cf22f0_

Production Deployment
---------------------
We recommend using PostgreSQL. Create a role and a database then grant all privileges to that role:

	sudo -u postgres psql

	CREATE ROLE roboconf WITH LOGIN PASSWORD 'foobar';
	CREATE DATABASE roboconf;
	GRANT ALL PRIVILEGES ON DATABASE roboconf to roboconf;

It is recommended to use `virtualenv`.

	cd staff.sitcon.org
	virtualenv venv
	. venv/bin/activate # if you use bash

Install dependencies.

	pip install -r requirements.txt

Copy example settings

	cp core/settings/local_settings.example.py core/settings/local_settings.py

	...

Load database schema and initial data

	python manage.py syncdb
	python manage.py loaddata */fixtures/*.json

_Note: currently there are problems with loaddata on `master` branch, see commit 5d8436149cf22f0_

	python manage.py collectstatic

Make media folder

	mkdir media
	chmod www-data:www-data media

Note on Python <2.7.9
---------------------

If you use Python <2.7.9, you need to install these extra packages for SSL SNI support, which OAuth client needs:

	pip install pyOpenSSL ndg-httpsclient

Ref: [https://stackoverflow.com/questions/18578439/using-requests-with-tls-doesnt-give-sni-support/18579484#18579484](https://stackoverflow.com/questions/18578439/using-requests-with-tls-doesnt-give-sni-support/18579484#18579484)

Naming
------
"Roboconf" pronounces familiar with 蘿蔔坑 (redish pit), from the Mandarin idiom "each redish has its own pit". Literally it stands for "robot-assisted conference" in English.

Developers
----------
* [Squirrel](https://github.com/azdkj532)
* [RSChiang](https://github.com/rschiang)
* [dv](https://github.com/wdv4758h)
* [pcchou](https://github.com/pcchou)
* [Pellaeon](https://github.com/pellaeon)

Contributing
------------
We welcome issue report, pull requests, and/or friends willing to join SITCON's preparation. Find us at irc.freenode.net #sitcon channel, or [send us a letter](mailto:contact@sitcon.org).

License
-------
This project (Roboconf) is temporarily licensed under [GNU AGPL-3.0](http://www.gnu.org/licenses/agpl-3.0.html) with one conditional statement:

> If #Roboconf were used to operate a conference with:
> (a) 200 or more participants or (b) 50 or more staff,
> the conference organizer would need to either
> (a) help promote SITCON by putting SITCON logo on the conference website, or
> (b) support SITCON by either donation or becoming one of SITCON's sponsor.
