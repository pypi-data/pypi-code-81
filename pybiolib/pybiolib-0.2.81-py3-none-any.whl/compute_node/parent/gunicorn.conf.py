# pylint: skip-file TODO: Remove this line
# Gunicorn configuration file

bind = '0.0.0.0:5000'
loglevel = 'info'
threads = 1
timeout = 300
workers = 1
