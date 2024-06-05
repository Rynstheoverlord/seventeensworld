from flask import Flask 
from flask_session import Session


def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'efjlier3oek333_qwdfj'
  app.config['SESSION_PERMANENT'] = False
  app.config['SESSION_TYPE'] = "filesystem"



  Session(app)

  from .views import views

  app.register_blueprint(views, url_prefix='/')

  return app