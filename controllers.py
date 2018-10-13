import time

import requests
from flask import request

from app import route


@route('/')
def hello_world():
    return "HELLO, WORLD!\n"


@route('/ping')
def ping():
    return "PONG\n"


@route('/data', methods=['POST'])
def data():
    data = request.get_data()
    return str(data)


@route('/io/delay/<int:sec>')
def httpbin_delay(sec):
    r = requests.get(f'http://httpbin.org/delay/{sec}')
    return str(r.status_code)


@route('/400')
def bad_request():
    from werkzeug.exceptions import BadRequest
    raise BadRequest("Fake BadRequest.")


@route('/foo')
def foo_bar_exception():
    from error_handler import FooBarException
    raise FooBarException("Fake BadRequest.")


@route('/type-error')
def server_error():
    # forcibly raise type error
    int(None)


@route('/sleep/<int:seconds>')
def sleep(seconds):
    time.sleep(seconds)
    return 'END TO SLEEP FOR %s\n' % seconds