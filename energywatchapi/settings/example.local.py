
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
STATIC_ROOT = '/home/administrator/www/api/mystatic/'
STATIC_URL='/static/'

MEDIA_ROOT = '/home/administrator/www/api/mymedia/'
MEDIA_URL='/media/'