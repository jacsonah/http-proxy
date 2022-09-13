from http.client import HTTPConnection
from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        server_connection = HTTPConnection(self.headers.get('Host'))
        server_connection.request(self.command, self.path)
        server_response = server_connection.getresponse()
        server_connection.close()

        http_version = '.'.join(str(server_response.version))
        client_response = f'HTTP/{http_version} {server_response.status} {server_response.reason}\r\n'

        for header in server_response.getheaders():
            client_response += f'{header[0]}: {header[1]}\r\n'

        client_response += '\r\n'
        client_response = client_response.encode()
        client_response += server_response.read()
        print(client_response)
        self.wfile.write(client_response)


SERVER_PORT = 9090

with HTTPServer(('localhost', SERVER_PORT), RequestHandler) as http_server:
    print(f'serving at port {SERVER_PORT}')
    http_server.serve_forever()
