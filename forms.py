from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import sqlalchemy

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

class BookingForm(FlaskForm):
    guest_email = StringField('Your Email',
                        validators=[DataRequired(), Email()])
    owner_email = StringField('Host Email',
                        validators=[DataRequired(), Email()])
    property_id = StringField('Property ID',
                        validators=[DataRequired(), Length(min=7, max=7)])
    start_date = DateField('Check In Date', validators=[DataRequired()])
    end_date = DateField('Check Out Date', validators=[DataRequired()])
    submit = SubmitField('Book')
