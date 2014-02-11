Utuputki
========

What is this ?
--------------
Utuputki is a very simple django program for allowing people to pick youtube videos for playback on video screen at LAN parties.
The whole thing consists of two apps: the player which is used on screen computer, and the manager app which users can use to add videos for playback. At the moment there is no user registration or anything like that, mostly because the app is expected to run in LAN behind firewalls.

Dependencies
------------
Requires django 1.6, django-crispy-forms, django-rosetta and south.

Quick installation: `pip install django django-crispy-forms django-rosetta south`

Installation
------------
1. Install dependencies
2. Copy `Utuputki/settings.py-dist` to `Utuputki/settings.py` and modify as necessary.
3. Do syncdb `./manage.py syncdb`
4. Do migration `./manage.py migrate`
5. If utuputki is not run in debug mode, you need to do collectstatic `./manage.py collectstatic`
6. Start server. If you're running the server in testing environment or just dont care, do `./manage.py runserver`

Translating
-----------
Utuputki comes with english and finnish translations at the moment. Translating to a new language can be done by copying the english translation into a new directory in locale/ directory, and then running http://localhost:8000/rosetta in debug mode.

License
-------
MIT. Please refer to `LICENSE` for more information.

Screenshots
-----------
![manager](https://github.com/katajakasa/utuputki/raw/master/screenshots/manager.png "Video manager")
![player](https://github.com/katajakasa/utuputki/raw/master/screenshots/player.png "Video player")
