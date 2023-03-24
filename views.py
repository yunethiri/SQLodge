from flask import request, Response, render_template, Blueprint, flash, url_for, redirect
from flask_login import login_required, current_user
import sqlalchemy
import json
from models import db
from decimal import Decimal
from typing import Dict
from forms import UpdateAccountForm, BookingForm
from models import session, Guests, Properties
from flask_admin import BaseView, expose
from datetime import datetime
from sqlalchemy import and_

posts = [
    {
        'author': 'ADMINS',
        'title': 'WELCOME',
        'content': 'WELCOME AGAIN',
        'date_posted': 'March 24, 2023'
    }
]

views = Blueprint('views', __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template('home.html', posts=posts, user=current_user)


@views.route("/")
@views.get("/listings")
@login_required
def get_relation():
    try:
        statement = sqlalchemy.text(f"SELECT * FROM PROPERTIES;")
        res = db.execute(statement)
        db.commit()
        data = generate_table_return_result(res)
        data = json.loads(data)
        return render_template('listings.html', title = 'Listings', table_data=data, user=current_user)
    except Exception as e:
        db.rollback()
        return Response(str(e), 403)


@views.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        property = session.query(Properties).filter(and_(Properties.owner==f'{form.owner_email.data}', Properties.property_id==f'{form.property_id.data}')).all()
        guest = session.query(Guests).filter_by(email=f'{form.guest_email.data}').first()
        if property and guest:
            start_date= form.start_date.data
            end_date = form.end_date.data
            # Check that the start date is not earlier than today's date
            if start_date < datetime.now().date():
                flash('Start date cannot be earlier than today.', category='error')
                return redirect(url_for('views.booking'))
            
            # Check that the end date is not earlier than the start date
            if end_date < start_date:
                flash('End date cannot be earlier than start date.', category='error')
                return redirect(url_for('views.booking'))
            
            duration = end_date - start_date
            days = duration.days
            # Insert the booking details into the database
            try:
                statement = sqlalchemy.text(f"INSERT INTO bookings VALUES ('{form.guest_email.data}', '{form.owner_email.data}', '{form.property_id.data}', '{form.start_date.data}',  '{form.end_date.data}', {days});")
                db.execute(statement)
                db.commit()
                flash('Your booking has been confirmed!', 'success')
                return redirect(url_for('views.booking'))
            except Exception as e:
                db.rollback()
                flash(str(e), 'error')
        else:
            if not guest:
                flash('Your email is not registered.', category='error')
                return redirect(url_for('views.booking'))
            else:
                flash('The host/property is not valid.', category='error')
                return redirect(url_for('views.booking'))
    
    return render_template('booking.html', title='Booking', form = form, user=current_user)

    
@views.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.email.data != current_user.email:
            guest = session.query(Guests).filter_by(email=f'{form.email.data}').first()
            if guest:
                flash('That email is taken. Please choose a different one.', category='error')
                return redirect(url_for('views.profile'))
            else:
                try:
                    statement = sqlalchemy.text(f"UPDATE guests SET email = '{form.email.data}' WHERE email = '{current_user.email}';")         
                    db.execute(statement)
                    db.commit()

                    guest = session.query(Guests).filter_by(email=f'{form.email.data}').first()
                    flash('Your account has been updated! Please log in again.', 'success')
                    return redirect(url_for('views.profile'))
                except Exception as e:
                    db.rollback()
                    return Response(str(e), 403)
    return render_template('profile.html', title='Profile', form=form, user=current_user)



# ? a flask decorator listening for POST requests at the url /table-create
@views.post("/table-create")
def create_table():
    # ? request.data returns the binary body of the POST request
    data = request.data.decode()
    try:
        # ? data is converted from stringified JSON to a Python dictionary
        table = json.loads(data)
        # ? data, or table, is an object containing keys to define column names and types of the table along with its name
        statement = generate_create_table_statement(table)
        # ? the remaining steps are the same
        db.execute(statement)
        db.commit()
        return Response(statement.text)
    except Exception as e:
        db.rollback()
        return Response(str(e), 403)


@views.post("/table-insert")
# ? a flask decorator listening for POST requests at the url /table-insert and handles the entry insertion into the given table/relation
# * You might wonder why PUT or a similar request header was not used here. Fundamentally, they act as POST. So the code was kept simple here
def insert_into_table():
    # ? Steps are common in all of the POST behaviors. Refer to the statement generation for the explanatory
    data = request.data.decode()
    try:
        insertion = json.loads(data)
        statement = generate_insert_table_statement(insertion)
        db.execute(statement)
        db.commit()
        return Response(statement.text)
    except Exception as e:
        db.rollback()
        return Response(str(e), 403)


@views.post("/table-update")
# ? a flask decorator listening for POST requests at the url /table-update and handles the entry updates in the given table/relation
def update_table():
    # ? Steps are common in all of the POST behaviors. Refer to the statement generation for the explanatory
    data = request.data.decode()
    try:
        update = json.loads(data)
        statement = generate_update_table_statement(update)
        db.execute(statement)
        db.commit()
        return Response(statement.text, 200)
    except Exception as e:
        db.rollback()
        return Response(str(e), 403)


@views.post("/entry-delete")
# ? a flask decorator listening for POST requests at the url /entry-delete and handles the entry deletion in the given table/relation
def delete_row():
    # ? Steps are common in all of the POST behaviors. Refer to the statement generation for the explanatory
    data = request.data.decode()
    try:
        delete = json.loads(data)
        statement = generate_delete_statement(delete)
        db.execute(statement)
        db.commit()
        return Response(statement.text)
    except Exception as e:
        db.rollback()
        return Response(str(e), 403)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)
    
def generate_table_return_result(res):
    # ? An empty Python list to store the entries/rows/tuples of the relation/table
    rows = []

    # ? keys of the SELECT query result are the columns/fields of the table/relation
    columns = list(res.keys())

    # ? Constructing the list of tuples/rows, basically, restructuring the object format
    for row_number, row in enumerate(res):
        rows.append({})
        for column_number, value in enumerate(row):
            rows[row_number][columns[column_number]] = value

    # ? JSON object with the relation data
    output = {}
    output["columns"] = columns  # ? Stores the fields
    output["rows"] = rows  # ? Stores the tuples

    """
        The returned object format:
        {
            "columns": ["a","b","c"],
            "rows": [
                {"a":1,"b":2,"c":3},
                {"a":4,"b":5,"c":6}
            ]
        }
    """
    # ? Returns the stringified JSON object
    return json.dumps(output, cls=CustomJSONEncoder)

    
def generate_delete_statement(details: Dict):
    # ? Fetches the entry id for the table name
    table_name = details["relationName"]
    id = details["deletionId"]
    # ? Generates the deletion query for the given entry with the id
    statement = f"DELETE FROM {table_name} WHERE id={id};"
    return sqlalchemy.text(statement)


def generate_update_table_statement(update: Dict):

    # ? Fetching the table name, entry/tuple id and the update body
    table_name = update["name"]
    id = update["id"]
    body = update["body"]

    # ? Default for the SQL update statement
    statement = f"UPDATE {table_name} SET "
    # ? Constructing column-to-value maps looping
    for key, value in body.items():
        statement += f"{key}=\'{value}\',"

    # ?Finalizing the update statement with table and row details and returning
    statement = statement[:-1]+f" WHERE {table_name}.id={id};"
    return sqlalchemy.text(statement)


def generate_insert_table_statement(insertion: Dict):
    # ? Fetching table name and the rows/tuples body object from the request
    table_name = insertion["name"]
    body = insertion["body"]
    valueTypes = insertion["valueTypes"]

    # ? Generating the default insert statement template
    statement = f"INSERT INTO {table_name}  "

    # ? Appending the entries with their corresponding columns
    column_names = "("
    column_values = "("
    for key, value in body.items():
        column_names += (key+",")
        if valueTypes[key] == "TEXT" or valueTypes[key] == "TIME":
            column_values += (f"\'{value}\',")
        else:
            column_values += (f"{value},")

    # ? Removing the last default comma
    column_names = column_names[:-1]+")"
    column_values = column_values[:-1]+")"

    # ? Combining it all into one statement and returning
    #! You may try to expand it to multiple tuple insertion in another method
    statement = statement + column_names+" VALUES "+column_values+";"
    return sqlalchemy.text(statement)


def generate_create_table_statement(table: Dict):
    # ? First key is the name of the table
    table_name = table["name"]
    # ? Table body itself is a JSON object mapping field/column names to their values
    table_body = table["body"]
    # ? Default table creation template query is extended below. Note that we drop the existing one each time. You might improve this behavior if you will
    # ! ID is the case of simplicity
    statement = f"DROP TABLE IF EXISTS {table_name}; CREATE TABLE {table_name} (id serial NOT NULL PRIMARY KEY,"
    # ? As stated above, column names and types are appended to the creation query from the mapped JSON object
    for key, value in table_body.items():
        statement += (f"{key}"+" "+f"{value}"+",")
    # ? closing the final statement (by removing the last ',' and adding ');' termination and returning it
    statement = statement[:-1] + ");"
    return sqlalchemy.text(statement)