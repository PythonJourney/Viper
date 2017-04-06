from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
from SocketServer import ThreadingMixIn

class Viper:

    glob_method_dict = {}

    def __init__(self):
        self.port = False # Default


    def setup(self, port):
        self.port = port
        self.server = HTTPServer(('localhost', self.port), self.HTTPRequestHandler)


    def run(self):
        self.server.serve_forever()


    def add_method(self, route, method_type, func):
        if not route.endswith('/'):
            print('ERROR at creating method ' + route + ': please follow the format - .*/url/')
            exit()
        Viper.glob_method_dict[route] = {'TYPE': method_type, 'FUNCTION': func}


    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        """Handling requests using multithreading"""


    class HTTPRequestHandler(BaseHTTPRequestHandler):

        def get_func_output(self, func):
            arg_dict = parse_qs(urlparse(self.path).query)
            args = list()
            for keys in arg_dict:
                args.append(arg_dict[keys])

            return func(*args)


        def get_method(self, ref, type):
            for key in Viper.glob_method_dict:
                if ref.endswith(key):
                    if Viper.glob_method_dict[key]['TYPE'] == type:
                        return key

            return False


        def get_request(self):
            print(self.path)
            if self.path[-1] == '/':
                ref = self.path.rsplit('/', 1)[0] + '/'
            else:
                ref = '/' + self.path.rsplit('/', 1)[1] + '/'

            print(ref)
            return ref


        def do_HEAD(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()


        def do_GET(self):
            method_ref = self.get_method(self.get_request(), 'GET')

            if not method_ref:
                self.send_response(400, 'Bad Request')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(self.get_func_output(Viper.glob_method_dict[method_ref]['FUNCTION']))


        def do_POST(self):
            method_ref = self.get_method(self.get_request(), 'POST')

            if not method_ref:
                self.send_response(400, 'Bad Request')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
            else:
                self.send_response(201)
                self.end_headers()
                self.wfile.write('Created')


        def do_DELETE(self):
            method_ref = self.get_method(self.get_request(), 'DELETE')

            if not method_ref:
                self.send_response(400, 'Bad Request')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
            else:
                self.send_response(301)
                self.end_headers()
                self.wfile.write('Deleted')


        def do_PUT(self):
            method_ref = self.get_method(self.get_request(), 'PUT')

            if not method_ref:
                self.send_response(400, 'Bad Request')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
            else:
                self.send_response(301)
                self.end_headers()
                self.wfile.write('Updated')

