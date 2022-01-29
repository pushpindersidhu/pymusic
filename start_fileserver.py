import http.server
import sys

KILL_SERVER_COMMAND = '/$kill-file-server'


def start_fileserver(host="localhost", port=80):


    class FileServerHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        stop_server = False
        base_directory = "C:\\"
        kill_server_command = KILL_SERVER_COMMAND

        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=self.base_directory, **kwargs)

        def address_string(self):
            host, port = self.client_address[:2]
            #return socket.getfqdn(host)
            return host

        def send_head(self):
            if self.path == FileServerHTTPRequestHandler.kill_server_command and self.address_string() == host:
                FileServerHTTPRequestHandler.stop_server = True
                return super().send_head()
            if self.path.startswith(FileServerHTTPRequestHandler.base_directory):
                return super().send_head()
            else:
                return super().send_head()
                # return self.send_error(404, "Not allowed", "The path you requested is forbidden.")

    httpd = http.server.HTTPServer((host, port), FileServerHTTPRequestHandler)
    print(f'http://{host}:{port}')
    while not FileServerHTTPRequestHandler.stop_server:
        httpd.handle_request()


if __name__ == '__main__':
    start_fileserver()
