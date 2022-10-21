"""
Basic HTTP web server to test the UI from
"""
import functools
import logging
import signal
import socketserver
from http.server import SimpleHTTPRequestHandler

DIRECTORY = "app/dist/spa"

Handler = functools.partial(SimpleHTTPRequestHandler, directory=DIRECTORY)


logger = logging.getLogger(__name__)

logger.debug("HTTP functions")


def run_http(port):
    """
    Run web server to serve UI
    """

    PORT = port

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        logging.info("Serving app on port %s", PORT)
        logging.warn("DO NOT use this server for production! Use NGINX")

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
