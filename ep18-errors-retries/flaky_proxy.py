"""
Episode 18 - a deliberately unreliable server, for testing.
It sits between our code and Ollama. The first FAILS requests get an error
(503 "overloaded" or 429 "too many requests"), after that it forwards to Ollama.
Run it in a second terminal:  python flaky_proxy.py 2
"""
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

FAILS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
OLLAMA = "http://localhost:11434"
seen = 0


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        global seen
        seen += 1
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if seen <= FAILS:
            code = 503 if seen % 2 else 429
            print(f"request {seen}: answering {code} on purpose", flush=True)
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": {"message": "simulated outage"}}')
            return
        print(f"request {seen}: forwarding to Ollama", flush=True)
        req = urllib.request.Request(OLLAMA + self.path, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as r:
            data = r.read()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


print(f"flaky proxy on http://localhost:11500, failing the first {FAILS} requests", flush=True)
ThreadingHTTPServer(("localhost", 11500), Handler).serve_forever()
