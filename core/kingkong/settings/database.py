# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "kingkong",
        "USER": "kingkong",
        "PASSWORD": PASSWORD,  # noqa
        "HOST": "localhost",
        "PORT": "5432",
    }
}
