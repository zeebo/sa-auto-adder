# Django settings for webinterface project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

APPEND_SLASH = False

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w7tlzg3y!59abpv@th!xzb+cxpi_#kwz(0q!4!)elb=5_r5ae$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'webinterface.urls'

ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    ROOT_PATH + "/templates"
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'appengine_utilities',
    'sa_auth',
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    'django.contrib.sites',
)


__author__="jbowman"
__date__ ="$Sep 11, 2009 4:20:11 PM$"
 
 
# Configuration settings for the session class.
session = {    
    "COOKIE_NAME": "gaeutilities_session",
    "DEFAULT_COOKIE_PATH": "/",
    "SESSION_EXPIRE_TIME": 7200,    # sessions are valid for 7200 seconds
                                    # (2 hours)
    "INTEGRATE_FLASH": True,        # integrate functionality from flash module?
    "SET_COOKIE_EXPIRES": True,     # Set to True to add expiration field to
                                    # cookie
    "WRITER":"datastore",           # Use the datastore writer by default. 
                                    # cookie is the other option.
    "CLEAN_CHECK_PERCENT": 50,      # By default, 50% of all requests will clean
                                    # the datastore of expired sessions
    "CHECK_IP": True,               # validate sessions by IP
    "CHECK_USER_AGENT": True,       # validate sessions by user agent
    "SESSION_TOKEN_TTL": 5,         # Number of seconds a session token is valid
                                    # for.
    "UPDATE_LAST_ACTIVITY": 60,     # Number of seconds that may pass before
                                    # last_activity is updated
}
 
# Configuration settings for the cache class
cache = {
    "DEFAULT_TIMEOUT": 3600, # cache expires after one hour (3600 sec)
    "CLEAN_CHECK_PERCENT": 50, # 50% of all requests will clean the database
    "MAX_HITS_TO_CLEAN": 20, # the maximum number of cache hits to clean
}
 
# Configuration settings for the flash class
flash = {
    "COOKIE_NAME": "appengine-utilities-flash",
}
 
# Configuration settings for the paginator class
paginator = {
    "DEFAULT_COUNT": 10,
    "CACHE": 10,
    "DEFAULT_SORT_ORDER": "ASC",
}
 
rotmodel = {
    "RETRY_ATTEMPTS": 3,
    "RETRY_INTERVAL": .2,
}
    
