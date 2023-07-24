from flask import Flask, request


def init_header_request_id(app: Flask):
    @app.after_request
    def append_request_id(response):
        request_id = request.headers.get('X-Request-Id')
        response.headers.add('X-Request-Id', request_id)
        return response
