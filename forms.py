from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, IntegerField, TextAreaField, RadioField, FloatField
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
    name = StringField('Name',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

class BookingForm(FlaskForm):
    guest_email = StringField('Your Email',
                        validators=[DataRequired(), Email()])
    owner_email = StringField('Host Email',
                        validators=[DataRequired(), Email()], render_kw={"disabled": True})
    # property_id = StringField('Property ID',
    #                     validators=[DataRequired(), Length(min=7, max=7)])
    property_id = IntegerField('Property ID',
                               validators=[DataRequired()])
    start_date = DateField('Check In Date', validators=[DataRequired()])
    end_date = DateField('Check Out Date', validators=[DataRequired()])
    submit = SubmitField('Book')

class FilterForm(FlaskForm):
    property_type = SelectField('Property Type', 
                                choices=[('None', 'All'), ('Apartment', 'Apartment'), ('House', 'House'), ('Condominium', 'Condominium'), ('Others','Others')])
    min_price = IntegerField('Minimum Price Per Night')
    max_price = IntegerField('Maximum Price Per Night')
    neighbourhood = SelectField('Neighbourhood', 
                            choices = [('None', 'All'), ('Pacific Beach','Pacific Beach'), ('Tierrasanta','Tierrasanta'), ('Rancho Penasquitos','Rancho Penasquitos'), ('Point Loma Heights','Point Loma Heights'), ('Mission Beach','Mission Beach'), ('East Village','East Village'), ('Park West','Park West'), ('Little Italy','Little Italy'), ('Cherokee Point','Cherokee Point'), ('North Park','North Park'), ('Bay Park','Bay Park'), ('Sherman Heights','Sherman Heights')])

    except_neighbourhood = SelectField('Except Neighbourhood', 
                                   choices=[('None', 'None'), ('Pacific Beach','Pacific Beach'), ('Tierrasanta','Tierrasanta'),('Rancho Penasquitos','Rancho Penasquitos'), ('Point Loma Heights','Point Loma Heights'),('Mission Beach','Mission Beach'), ('East Village','East Village'), ('Park West','Park West'), ('Little Italy','Little Italy'), ('Cherokee Point','Cherokee Point'), ('North Park','North Park'), ('Bay Park','Bay Park'), ('Sherman Heights','Sherman Heights')])
    sort_by = RadioField('Sort by', choices=[('ASC', 'Price Per Night: Low to High'), ('DESC', 'Price Per Night: High to Low')]
                         , default = ('ASC', 'Price Per Night: Low to High'))
    submit = SubmitField('Filter')

class UpdatePropertiesForm(FlaskForm):
   property_id = IntegerField('Property ID', validators=[DataRequired()])
   price_per_night = FloatField('Price Per Night', validators=[DataRequired()])
   accommodates = IntegerField('Accommodates', validators=[DataRequired()])
   amenities = TextAreaField('Amenities Available', validators=[DataRequired()])
   submit = SubmitField('Update')

class StatsForm(FlaskForm):
    email = StringField('Host Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
