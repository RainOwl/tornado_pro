#_author_ : duany_000
#_date_ : 2018/2/6
import tornado.ioloop
import tornado.web
import time
from tornado import gen
from tornado.concurrent import Future

class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        from tornado import httpclient
        http = httpclient.AsyncHTTPClient()
        yield http.fetch("http://www.google.com", self.done)
    def done(self):
        self.write("Hello, main")
        self.finish()

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
    application.listen(9001)
    tornado.ioloop.IOLoop.instance().start()
