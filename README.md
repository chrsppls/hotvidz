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