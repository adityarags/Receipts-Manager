from flask import Flask
import os
import pandas as pd
from application.config import Config
from application.database import db
# import webview

app = None
curr_dir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__, template_folder = "templates")
    app.config.from_object(Config)
    app.app_context().push()
    return app

app = create_app()

db.init_app(app)


# window = webview.create_window("NGO Receipts Mannager", app)


if __name__ == "__main__":
    from application.controllers import *
    app.run()
    # webview.start()