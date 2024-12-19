#!/bin/sh

daphne -b 0.0.0.0 -p 8001 mysite.asgi:application