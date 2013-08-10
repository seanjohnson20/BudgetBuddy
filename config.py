import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'LJyyfy8A2MQEI9GynmXkCSVlXIRPUp76'
DEBUG = True
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
