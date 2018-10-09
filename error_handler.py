from werkzeug.exceptions import BadRequest

from app import app
from exceptions import FooBarException


@app.errorhandler(BadRequest)
def handle_bad_request(e):
	return 'BAD REQUEST', 400


@app.errorhandler(FooBarException)
def handle_fooBarExcaption(e):
	return "FooBarException", 400