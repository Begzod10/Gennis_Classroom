#!/venv python3
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8
from flask import *
from backend.models.basic_model import *
from flask_cors import CORS
from pprint import pprint
from werkzeug.utils import *
import os
import json

app = Flask(__name__, static_folder="frontend/build", static_url_path="/")
app.config.from_object('backend.models.config')
db = db_setup(app)
migrate = Migrate(app, db)
CORS(app)
api = '/api'
# basics
from backend.basics.views import *
# create basics
from backend.create_basics.views import *

# student
from backend.student.views import *

if __name__ == '__main__':
    app.run()
