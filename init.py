import uuid
from flask import Flask
from database import *

user = User()
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
