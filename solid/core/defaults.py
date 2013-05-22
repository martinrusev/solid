import sys
try:
    import json
except ImportError:
    import simplejson as json

try:
    config_file = file('/etc/solid.conf').read()
    config = json.loads(config_file)
except Exception, e:
    print "There was an error in your configuration file (/etc/solid.conf)"
    raise e

#  Amon Defaults
MONGO = config.get('mongo', "mongodb://127.0.0.1:27017")

_web_app = config.get('web_app', {})

host = _web_app.get('host', 'http://127.0.0.1')

if not host.startswith('http'):
    host = "http://{0}".format(host)

WEB_APP = {
        'host': host,
        'port': _web_app.get('port', 6464)
        }

key = config.get('secret_key', None)

if key != None and len(key) > 0:
    SECRET_KEY = key
else:
    SECRET_KEY = 'p86f9cfgEuvl4HFGthR1TBAUE7Sfiz8NoDGTeNHh7Sw' #Don't break the dashboard

# Always 
ACL = 'True'

TIMEZONE = config.get('timezone','UTC')

PROXY = config.get('proxy', None) # Relative baseurl if true
LOGFILE = config.get("logfile", '/var/log/solid/solid.log')