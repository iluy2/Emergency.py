from flaskwebgui import FlaskUI

from init import app
from routes import *

if __name__ == "__main__":
    FlaskUI(app=app, server="flask", width=800, height=600).run()
