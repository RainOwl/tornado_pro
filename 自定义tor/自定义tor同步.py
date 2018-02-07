#_author_ : duany_000
#_date_ : 2018/2/6
import socket
import select

def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind(("127.0.0.1",9002))
    sock.setblocking(False)
    sock.listen(123)

    inputs = []
    inputs.append(sock)

    while True:
        rlist,wlist,elist = select.select(inputs,[],[],0.06)
        # print("rlist-->",rlist)
        for r in rlist:
            if r==sock:
                """第一次请求"""
                conn,addr = sock.accept()
                conn.setblocking(False)
                inputs.append(conn)
            else:
                """客户端发送数据"""
                data = b""
                while True:
                    try:
                        chunk = r.recv(1024)
                        data +=chunk
                    except Exception as e:
                        chunk = None
                    if not chunk:
                        break
                # data进行处理：请求头和请求体
                print("data-->",data)
                request = HttpRequest(data)
                print('request-->',request)
                # 1. 请求头中获取url
                # 2. 去路由中匹配，获取指定的函数
                # 3. 执行函数，获取返回值
                # 4. 将返回值 r.sendall
                import re
                flag = False
                print("request.url-->", request.url)
                for route in routers:
                    print('route-->',route)
                    if re.match(route[0],request.url):
                        flag = True
                        func = route[1]
                        print('func-->',func)
                        break
                if flag:
                    result = func(request)
                    # print("result-->",result)
                    # r.sendall(bytes(result, encoding='utf-8'))
                    result = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n%s\r\n'%result
                    # result = str(data,encoding='utf-8')+result
                    r.sendall(bytes(result,encoding='utf-8'))
                else:
                    r.sendall(b'404')
                inputs.remove(r)
                r.close()



class HttpRequest(object):
    """
    用户封装：用户请求信息
    """
    def __init__(self,content):
        """
        用户发送的请求数据：请求头和请求体
        """
        self.content = content
        self.header_bytes = bytes()
        self.body_bytes = bytes()

        self.header_dict = {}

        self.method = ''
        self.url = ''
        self.protocol = ''

        self.initialize()
        self.initialize_headers()

    def initialize(self):
        temp = self.content.split(b'\r\n\r\n', 1)
        if len(temp)==1:
            self.header_bytes += temp[0]
        else:
            h,b = temp
            self.header_bytes += h
            self.body_bytes += b

    @property
    def header_str(self):
        return str(self.header_bytes,encoding='utf8')

    def initialize_headers(self):
        print("self.header_str-->",self.header_str)
        headers = self.header_str.split('\r\n')
        first_line = headers[0].split(' ')
        if len(first_line)==3:
            self.method,self.url,self.protocol = headers[0].split(' ')
            print('self.url-->',self.url)
            for line in headers:
                kv = line.split(':')
                if len(kv)==2:
                    k,v = kv
                    self.header_dict[k] = v


def main(request):
    print('main')
    return "main"

def index(request):
    print('index')
    return "indexasdfasdfasdf"


routers = [
    ('/main/',main),
    ('/index/',index),
]


if __name__ == '__main__':
    run()




