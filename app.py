from flask import Flask


app = Flask(__name__)
route = app.route


from controllers import *
from error_handler import *
