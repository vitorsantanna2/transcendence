if IN_DOCKER:
    print("IN_DOCKER is True")
    assert MIDDLEWARE[:1] == [
        'django.middleware.security.SecurityMiddleware'
    ]