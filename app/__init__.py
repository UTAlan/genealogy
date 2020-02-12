from config import Config
from flask import Flask
import os

UPLOAD_FOLDER = os.path.abspath("/uploads")

app = Flask(__name__, static_url_path='', static_folder="static", template_folder="templates")

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes
