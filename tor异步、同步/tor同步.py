#_author_ : duany_000
#_date_ : 2018/2/6
import tornado.ioloop
import tornado.web
import time
from tornado import gen

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        time.sleep(10)
        self.write("Hello, main")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, index")


settings = {
    'template_path':'templates',
}
application = tornado.web.Application([
    (r"/index", IndexHandler),
    (r"/main", MainHandler),
],**settings)

if __name__ == "__main__":
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()
