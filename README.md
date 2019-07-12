Aplikacja WWW
=============

Django-based application to manage registration of people for [scientific summer school](https://warsztatywww.pl/).

### Build:
- install `python3` and `pip3`
- `python3 -m venv venv` - create a virtual python environment for the app
- `source venv/bin/activate` - activate venv
- `./migrate.sh` - apply DB migrations
- `./manage.py createsuperuser` - script to create a superuser that can modify DB contents via admin panel
- `./manage.py populate_db` - script to populate the database with data for development

### Run:
- activate virtualenv (if not yet activated)
- `pip install -r requirements.txt`
- `./runserver.sh`

### Online version:
App currently available at https://warsztatywww.pl/
