
import  os
BASE_DIR     = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.getenv("DB_NAME"),        # Or path to database file if using sqlite3.
        'USER': os.getenv('DB_USER'),                   # Not used with sqlite3.
        'PASSWORD': os.getenv('DB_PASSWORD'),            # Not used with sqlite3.
        'HOST': os.getenv('DB_HOST'),             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': os.getenv('DB_PORT'),                  # Set to empty string for default. Not used with sqlite3.
    }
}

# DATABASES = {
#      'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'wvapi',        # Or path to database file if using sqlite3.
#         'USER': 'wvuser',                   # Not used with sqlite3.
#         'PASSWORD': '#wvuser',            # Not used with sqlite3.
#         'HOST': 'localhost',             # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '5432',                  # Set to empty string for default. Not used with sqlite3.
#     }
# }

import sys
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }
# pg_dump -U nzmewqyrvjyhpl -h ec2-107-22-173-160.compute-1.amazonaws.com dcoimmfelmkfbc > winda_backup

# Update database configuration with $DATABASE_URL.
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATIC_ROOT = os.getenv("STATIC_ROOT")

STATIC_URL='/static/'

MEDIA_ROOT = os.getenv("MEDIA_ROOT")
MEDIA_URL='/media/'

# Extra places for collectstatic to find static files.
EMAIL_USE_SSL = True
EMAIL_HOST=os.getenv("EMAIL_HOST")
EMAIL_HOST_USER=os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD= os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")



STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, '../../templates'),

)


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'