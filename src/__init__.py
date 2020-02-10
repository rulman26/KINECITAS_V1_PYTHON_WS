from flask import Flask,make_response,jsonify
from flask_cors import CORS
from config import DevelopmentConfig,ProductionConfig,TestingConfig
from .usuario.controller import usuario
from .kinecita.controller import kinecita
import os
app = Flask(__name__)
CORS(app)
app_settings = os.getenv('APP_SETTINGS',DevelopmentConfig)
app.config.from_object(app_settings)
app.register_blueprint(usuario,url_prefix='/api/usuario')
app.register_blueprint(kinecita,url_prefix='/api/kinecita')