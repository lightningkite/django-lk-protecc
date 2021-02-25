import os

def settings(BASE_DIR=os.getcwd()):

    SECRET_KEY = 'fake-key'

    DEBUG = True

    ALLOWED_STRIKES = 3

    SITE_NAME = 'fake-project'

    ADMIN_EMAIL = 'example@gmail.com'

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        },
    }

    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.admin',
        'django_lk_protecc.protecc',
    ]

    MIDDLEWARE_CLASSES = ()

    MIDDLEWARE = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.contrib.messages.middleware.SessionMiddeware",
    ]

    # Template loading
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'dev_db',
        }
    }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

    return {key: value for (key, value) in vars().items() if key.isupper()}
