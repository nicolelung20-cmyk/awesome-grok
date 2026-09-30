"""Serve dashboard.html on 127.0.0.1 only (not reachable from other machines)."""
import http.server, functools, sys
from pathlib import Path

import build

HERE = Path(__file__).parent


class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] not in ("/", "/dashboard.html"):
            return self.send_error(404)
        (HERE / "dashboard.html").write_text(build.render() + "\n")
        self.path = "/dashboard.html"
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(H, directory=str(HERE)))
    print(f"http://127.0.0.1:{port}  (local only, Ctrl-C to stop)")
    srv.serve_forever()
