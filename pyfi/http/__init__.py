import socketserver
import http
import functools
import logging
import signal

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
            "DO NOT use the app web server on port %s for production! Use NGINX", PORT)

        def http_shutdown():
            """
            Handle any cleanup here
            """
            # Kill all processes
            httpd.shutdown()

        signal.signal(signal.SIGINT, http_shutdown)

        try:
            httpd.serve_forever()
        except:
            pass
