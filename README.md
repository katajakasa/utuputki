Utuputki
========

PLEASE NOTE! THIS PROJECT IS DEPRECATED! See [Utuputki2](https://github.com/katajakasa/Utuputki2) for the new project!

What is this ?
--------------
Utuputki is a very simple django program for allowing people to pick youtube videos for playback on video screen at LAN parties.
The whole thing consists of two apps: the player which is used on screen computer, and the manager app which users can use to add videos for playback. At the moment there is no user registration or anything like that, mostly because the app is expected to run in LAN behind firewalls.

Dependencies
------------
Requirements:
* django 1.8
* django-crispy-forms
* django-rosetta

Quick installation: `pip install -r deploy/requirements.txt`

Installation
------------
1. Install dependencies
2. Copy `Utuputki/settings.py-dist` to `Utuputki/settings.py` and modify as necessary. Fill in at least  SECRET_KEY.
3. Run database migrations `python manage.py migrate`
4. Create a superuser `python manage.py createsuperuser`.
5. Start server. If you're running the server in testing environment or just don't care, do `python manage.py runserver`.
   Otherwise, please see django deployment guides.

StreamCli
---------

Streamcli is a client for utuputki, which uses a GTK window to stream the videos. May work better than the HTML5 client.

Additional requirements (python bindings + possible system libs):
* PyGObject
* GTK+ 3
* GStreamer
* Livestreamer (`pip install livestreamer`)
* VLC player (in path)

For PyGObject for windows python, see [PyGObjectWin32](http://sourceforge.net/projects/pygobjectwin32/). This should contain
all the required packages.

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
