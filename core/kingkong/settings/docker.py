if IN_DOCKER:  # noqa
    print("IN_DOCKER is True")
    assert MIDDLEWARE[:1] == ["django.middleware.security.SecurityMiddleware"]  # noqa
