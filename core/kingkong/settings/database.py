# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "artemis",
        "USER": "postgres",
        "PASSWORD": POSTGRES_PW,  # noqa
        "HOST": "postgres",
        "PORT": "5432",
    }
}
