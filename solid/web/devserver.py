import sys
sys.path.insert(0,'/home/martin/solid')

from solid.web.server import application
import tornado.ioloop
from solid.core import settings
from tornado import autoreload

if __name__ == "__main__":
    application.listen(int(settings.WEB_APP['port']))
    ioloop = tornado.ioloop.IOLoop().instance()
    autoreload.start(ioloop)
    ioloop.start()
