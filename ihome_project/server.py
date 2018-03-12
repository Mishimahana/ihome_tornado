#coding=utf-8
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define,options
import tornado.httpserver
import os
import redis
import torndb

import config
from urls import urls



define("port", default=8000, type=int, help="run server on the given port")
class Application(tornado.web.Application):
	def __init__(self,*args,**kwargs):
		super(Application,self).__init__(*args,**kwargs)
		self.db = torndb.Connection(**config.mysql_options)
		self.redis = redis.StrictRedis(**config.redis_options)


def main():
	options.log_file_prefix = config.log_path
	options.logging = config.log_level
	tornado.options.parse_command_line()
	app = Application(urls,**config.settings)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
 	tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
	main()