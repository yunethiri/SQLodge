from flask import Flask
from json2html import *
from flask_login import LoginManager
from flask_admin import Admin
from models import Users, Properties, Bookings, session
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

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
        return session.query(Users).get(email)
    
    admin = Admin(app, template_mode="bootstrap4")
    admin.add_view(ModelView(Users, session))
    admin.add_view(ModelView(Properties, session))
    admin.add_view(ModelView(Bookings, session))

    class MyView(BaseView):
        @expose("/")
        def index(self):
            return self.render('index.html')

    return app


data_types = {
    'boolean': 'BOOL',
    'integer': 'INT',
    'text': 'TEXT',
    'time': 'TIME',
}
