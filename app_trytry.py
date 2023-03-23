from flask import Flask
from json2html import *
from flask_login import LoginManager
from models import Guests, session

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '52e0e783a4456fdef0c336bbf207eed8'

    from auth import auth
    from views import views
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(email):
        return session.query(Guests).get(email)

    return app


data_types = {
    'boolean': 'BOOL',
    'integer': 'INT',
    'text': 'TEXT',
    'time': 'TIME',
}




