from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

from aozora_scraper import fetch_author_works, fetch_html, extract_text_from_html


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/works":
            qs = parse_qs(parsed.query)
            author_url = qs.get("author_url", [None])[0]
            if not author_url:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error":"author_url parameter required"}')
                return
            works = fetch_author_works(author_url)
            data = json.dumps({"works": works}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(data)
        elif parsed.path == "/work":
            qs = parse_qs(parsed.query)
            work_url = qs.get("url", [None])[0]
            if not work_url:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error":"url parameter required"}')
                return
            html = fetch_html(work_url)
            text = extract_text_from_html(html)
            data = json.dumps({"text": text}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()


def run(server_class=HTTPServer, handler_class=Handler) -> None:
    server_address = ("", 8000)
    httpd = server_class(server_address, handler_class)
    print("Serving on port 8000...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
