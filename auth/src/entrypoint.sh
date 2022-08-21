#!/bin/bash

#gunicorn -k gevent -w 4 wsgi_app:create_app --chdir Auth
gunicorn -k gevent -w 4 wsgi_app:create_app