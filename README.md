# Hotvidz Readme

### Initiating Heroku

##Login to Heroku

1. heroku login
2. heroku create
3. git push heroku master


## Additions to heroku
Static Files
1. pip install whitenoise
2. Add to settings: STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
3. Add to settings > MIDDLEWARE: 'whitenoise.middleware.WhiteNoiseMiddleware'

## Allowed hosts
1. Add to settings: ALLOWED_HOSTS: heroku generated url ex. 'agile-earth-50687.herokuapp.com/'

## Create a Procfile
1. Create Procfile
2. Include the following:
```
release: python manage.py migrate
web: gunicorn.hotvidz.wsgi
```

## Create a Runtime
1. Create runtime.txt
2. Include the following:
```
python-3.9.0
```

## Load Seed Data from databases
1. heroku run python manage.py loaddata hotvidz.json

## Heroku open from CLI
1. heroku open