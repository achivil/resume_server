import gevent.pool
from gevent.wsgi import WSGIServer
from upload_server import app

MAXNUM = 10
spawn = gevent.pool.Pool(MAXNUM)
http_server = WSGIServer(('', 5000), app, spawn=spawn)
http_server.serve_forever()
