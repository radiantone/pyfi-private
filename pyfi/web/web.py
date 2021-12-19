"""
Basic HTTP web server to test the UI from
"""
import functools
import http
import logging
import signal
import socketserver

DIRECTORY = "app/dist/spa"

Handler = functools.partial(
    http.server.SimpleHTTPRequestHandler, directory=DIRECTORY)


def run_http(port):
    """
    Run web server to serve UI
    """
    import http.server

    PORT = port

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        logging.info("Serving app on port %s", PORT)
        logging.warn(
            "DO NOT use this server for production! Use NGINX")

        def http_shutdown():
            """
            Handle any cleanup here
            """
            httpd.shutdown()

        signal.signal(signal.SIGINT, http_shutdown)

        try:
            httpd.serve_forever()
        except Exception:
            pass
