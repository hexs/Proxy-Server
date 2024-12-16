from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

class ProxyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        target_url = f"http://192.168.137.11:8080{self.path}"
        with requests.get(target_url, headers=self.headers, stream=True) as response:
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.end_headers()

            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    self.wfile.write(chunk)
                    self.wfile.flush()

    def do_POST(self):
        target_url = f"http://192.168.137.11:8080{self.path}"
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        response = requests.post(target_url, headers=self.headers, data=body, stream=True)
        self.send_response(response.status_code)
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.content)

def run_server(server_class=HTTPServer, handler_class=ProxyRequestHandler, port=5000):
    server_address = ('192.168.1.103', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting proxy server on http://{server_address[0]}:{server_address[1]}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
