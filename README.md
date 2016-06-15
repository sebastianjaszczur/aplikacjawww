Aplikacja WWW
=============

Django-based application to manage registration of people for [scientific summer school](http://warsztatywww.pl/).

### Build:
- install `virtualenv` and `pip`
- `virtualenv venv` - create a virtual python environment for the app
- `source venv/bin/activate` - activate venv
- `./migrate.sh` - apply DB migrations
- `./manage.py createsuperuser` - script to create a superuser that can modify DB contents via admin panel

### Run:
- activate virtualenv (if not yet activated)
- `pip install -r requirements.txt`
- `./runserver.sh`

### Online version:
App currently available at http://warsztatywww.pl/
Also: http://aplikacjawww-jaszczur.rhcloud.com/
