import http.server

KILL_SERVER_COMMAND = '/$kill-file-server'


def start_fileserver(host="127.0.0.1", port=1984):
    class FileServerHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        stop_server = False
        base_directory = "/"
        kill_server_command = KILL_SERVER_COMMAND

        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory='/', **kwargs)

        def send_head(self):
            if self.path == FileServerHTTPRequestHandler.kill_server_command and self.address_string() == host:
                FileServerHTTPRequestHandler.stop_server = True
                return super().send_head()
            if self.path.startswith(FileServerHTTPRequestHandler.base_directory):
                return super().send_head()
            else:
                return self.send_error(404, "Not allowed", "The path you requested is forbidden.")

    httpd = http.server.HTTPServer((host, port), FileServerHTTPRequestHandler)
    httpd.timeout = 1
    while not FileServerHTTPRequestHandler.stop_server:
        httpd.handle_request()


if __name__ == '__main__':
    start_fileserver()
