# api/run.py

from http.server import BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data)
        
        code = request_data.get('code', '')
        
        try:
            # Execute the Python code
            exec_globals = {}
            exec(code, exec_globals)
            output = exec_globals.get('output', '')  # Fetch output from globals if defined
            response = {'output': output}
            self._set_headers(200)
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            # Return error message in case of an exception
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
