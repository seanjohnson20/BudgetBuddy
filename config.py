import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'LJyyfy8A2MQEI9GynmXkCSVlXIRPUp76'
DEBUG = True
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

stripe_keys = {
    'secret_key': 'sk_test_A7KRDPi2LZvfxvGF6IQVIwXz',
    'publishable_key': 'pk_test_0NGYO7LIaEAfOKMeG0JxJGoW'
}