from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistrationForm
from models import session, Users
from flask import request, Response, render_template, url_for, flash, redirect
import sqlalchemy

engine = sqlalchemy.create_engine(
    "postgresql://postgres:postgres@localhost/postgres"
)
db = engine.connect()

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = session.query(Users).filter_by(email=f'{form.email.data}',password=f'{form.password.data}').first()
            #statement = sqlalchemy.text(f"SELECT * FROM users WHERE email='{form.email.data}' AND password='{form.password.data}';")
            #guest = session.execute(statement).first()
            if user:
                flash(f'Login Successful for {form.email.data}', 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
                return redirect(url_for('auth.login'))
            
    return render_template('login.html', title='Login', form=form, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user = None
    if request.method == 'POST':
        if form.validate_on_submit():
            #user = session.query(Users).filter_by(email=f'{form.email.data}',password=f'{form.password.data}').first()
            statement = sqlalchemy.text(f"SELECT * FROM users WHERE email='{form.email.data}' AND password='{form.password.data}';")
            user = session.execute(statement).first()
            if user:
                flash('Email already exists.', category='error')
                return redirect(url_for('auth.register'))
            
            else:
                try:
                    statement = sqlalchemy.text(f"INSERT INTO users VALUES ('{form.username.data}', '{form.email.data}', '{form.password.data}');")            
                    db.execute(statement)
                    db.commit()
                    
                    user = session.query(Users).filter_by(email=f'{form.email.data}',password=f'{form.password.data}').first()
                    #statement = sqlalchemy.text(f"SELECT * FROM users WHERE email='{form.email.data}' AND password='{form.password.data}';")
                    #user = session.execute(statement).first()
                    login_user(user, remember=True)
                    flash(f'Account created for {form.username.data}!', 'success')
                    return redirect(url_for('views.home'))
                except Exception as e:
                    db.rollback()
                    return Response(str(e), 403)
        
    return render_template('register.html', title='Register', form=form, user=current_user)
