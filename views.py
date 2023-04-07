from flask import request, Response, render_template, Blueprint, flash, url_for, redirect
from flask_login import login_required, current_user
import sqlalchemy
import json
from models import db
from decimal import Decimal
from typing import Dict
from forms import UpdateAccountForm, BookingForm, FilterForm, UpdatePropertiesForm, StatsForm
from models import session, Users, Properties
from flask_admin import BaseView, expose
from datetime import datetime
from sqlalchemy import and_
import logging

posts = [
    {
        'author': 'ADMINS',
        'title': 'WELCOME',
        'content': 'Properties are available under Listings',
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
@views.route("/listings", methods=["GET", "POST"])
@login_required
def get_relation():
    try:
        form = FilterForm()
        statement = sqlalchemy.text(f"SELECT * FROM PROPERTIES;")
        res = db.execute(statement)
        data = generate_table_return_result(res)
        data = json.loads(data)

        if form.validate_on_submit():
            property_type = form.property_type.data
            min_price = form.min_price.data
            max_price = form.max_price.data
            neighbourhood = form.neighbourhood.data
            except_neighbourhood = form.except_neighbourhood.data
            sort_by = form.sort_by.data
            
            statement = f"SELECT * FROM PROPERTIES"
            if property_type:
                if (property_type == 'None'):
                    statement += f" INTERSECT (SELECT * from properties WHERE property_type !='{property_type}')"
                elif (property_type == 'Others'):
                    statement += f" INTERSECT (SELECT * from properties WHERE property_type NOT IN ('House', 'Apartment', 'Condominium'))"
                else:
                    statement += f" INTERSECT (SELECT * from properties WHERE property_type ='{property_type}')"
            if min_price:
                statement += f" INTERSECT (SELECT * from properties WHERE price_per_night >= {min_price})"
            if max_price:
                statement += f" INTERSECT (SELECT * from properties WHERE price_per_night <= {max_price})"
            if neighbourhood:
                if (neighbourhood == 'None'):
                    statement += f" INTERSECT (SELECT * from properties WHERE neighbourhood !='{neighbourhood}')"
                else:
                    statement += f" INTERSECT (SELECT * from properties WHERE neighbourhood ='{neighbourhood}')"
            if except_neighbourhood:
                if (except_neighbourhood == 'None'):
                    statement += f" INTERSECT (SELECT * from properties WHERE neighbourhood !='{except_neighbourhood}')"
                else:
                    statement += f" EXCEPT (SELECT * from properties WHERE neighbourhood ='{except_neighbourhood}')"
            if sort_by:
                statement += f" ORDER BY price_per_night {sort_by}"
    
            statement = sqlalchemy.text(statement)
            listings = db.execute(statement)
            listings = generate_table_return_result(listings)
            listings = json.loads(listings)
            return render_template('listings.html', title='Listings', form=form, table_data=listings, user=current_user)
        return render_template('listings.html', title='Listings', form=form, table_data=data, user=current_user)

    except Exception as e:
        db.rollback()
        return Response(str(e), 403)

@views.route("/")
@views.route("/mylistings", methods=["GET", "POST"])
@login_required
def get_my_listings():
    try:
        statement = sqlalchemy.text(f"SELECT * FROM properties where owner = '{current_user.email}';")
        res = db.execute(statement)
        data = generate_table_return_result(res)
        data = json.loads(data)
        return render_template('myownlistings.html', title='My Listings', table_data=data, user=current_user)

    except Exception as e:
        db.rollback()
        return Response(str(e), 403)

@views.route('/updatemylistings', methods=['GET', 'POST'])
@login_required
def update_listings():
    form = UpdatePropertiesForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            statement = sqlalchemy.text(f"UPDATE properties SET price_per_night = '{form.price_per_night.data}', accomodates  = '{form.accommodates.data}', amenities = '{form.amenities.data}' WHERE property_id = '{form.property_id.data}';")
            db.execute(statement)
            db.commit()
            flash('Your listing has been updated!', 'success')
            return redirect(url_for('views.get_my_listings'))
        except Exception as e:
            db.rollback()
            return Response(str(e), 403)
    property_id = request.args.get('property_id')
    form.property_id.data = property_id
    statement = sqlalchemy.text(f"SELECT * FROM properties WHERE property_id = {property_id}")
    res = db.execute(statement)
    data = json.loads(generate_table_return_result(res))
    form.price_per_night.data = data['rows'][0]['price_per_night']
    form.accommodates.data = data['rows'][0]['accomodates']
    form.amenities.data = data['rows'][0]['amenities']
    return render_template('updatemylistings.html', title='Update Listings', form=form, user=current_user)  

@views.route('/delete_entry', methods=['POST'])
def delete_entry():
    id = request.args.get('id')
    statement = sqlalchemy.text(f"DELETE FROM properties WHERE property_id = {id};")
    db.execute(statement)
    db.commit()
    flash('Property deleted successfully!', 'success')
    return redirect(url_for('views.get_my_listings'))

@views.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    form = BookingForm()
    property, users = None, None
    property_id = request.args.get('property_id')
    logging.warning(property_id)
    form.property_id.data = property_id
    statement = sqlalchemy.text(f"SELECT owner FROM PROPERTIES WHERE property_id = '{form.property_id.data}' ;")
    res = db.execute(statement)
    data = json.loads(generate_table_return_result(res))
    form.owner_email.data = data['rows'][0]['owner']
    if form.validate_on_submit():
        try:
            statement = sqlalchemy.text(f"SELECT * FROM users u WHERE u.email='{form.guest_email.data}';")
            guest = db.execute(statement)
            db.commit()
        except Exception as e:
            db.rollback()
            flash(str(e), 'error')     
        try:
            start_date= form.start_date.data
            end_date = form.end_date.data
            # Check that the start date is not earlier than today's date
            if start_date < datetime.now().date():
                flash('Start date cannot be earlier than today.', category='error')
                #return redirect(url_for('views.booking'))
                return redirect(f"/booking?property_id={form.property_id.data}")
            
            # Check that the end date is not earlier than the start date
            if end_date < start_date:
                flash('End date cannot be earlier than start date.', category='error')
                #return redirect(url_for('views.booking'))
                return redirect(f"/booking?property_id={form.property_id.data}")
            
            # Check that booking dates do not overlap with existing bookings
            statement = sqlalchemy.text(f"SELECT * FROM bookings WHERE property_id ='{form.property_id.data}' AND (('{form.start_date.data}' BETWEEN start_date AND end_date) OR ('{form.end_date.data}' BETWEEN start_date AND end_date));")
            conflict_booking = db.execute(statement).fetchall()
            if conflict_booking:
                flash('Booking dates conflict with another booking on this property.', category='error')
                #return redirect(url_for('views.booking'))
                return redirect(f"/booking?property_id={form.property_id.data}")
            duration = end_date - start_date
            days = duration.days
        except Exception as e:
            db.rollback()
            flash(str(e), 'error')  
        try:
            statement = sqlalchemy.text(f"INSERT INTO bookings VALUES ('{form.guest_email.data}', '{form.owner_email.data}', '{form.property_id.data}', '{form.start_date.data}',  '{form.end_date.data}', {days});")
            db.execute(statement)
            db.commit()
            flash('Your booking has been confirmed!', 'success')
            return redirect(f"/booking?property_id={form.property_id.data}")
        except sqlalchemy.exc.SQLAlchemyError as e:
            db.rollback()
            flash('Your email must match your account email.', category='error')
            return redirect(f"/booking?property_id={form.property_id.data}")
    return render_template('booking.html', title='Booking', form = form, user=current_user)

    
# @views.route("/profile", methods=['GET', 'POST'])
# @login_required
# def profile():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.email.data != current_user.email:
#             #guest = session.query(users).filter_by(email=f'{form.email.data}').first()
#             statement = sqlalchemy.text(f"SELECT * FROM users u WHERE u.email='{form.email.data}';")
#             guest = db.execute(statement).fetchone()
#             db.commit()
#             if guest:
#                 guest = generate_table_return_result(guest)
#                 guest = json.loads(guest)
#                 flash('That email is taken. Please choose a different one.', category='error')
#                 return redirect(url_for('views.profile'))
#             else:
#                 try:
#                     statement = sqlalchemy.text(f"UPDATE users u SET u.email = '{form.email.data}' WHERE u.email = '{current_user.email}';")       
#                     db.execute(statement)
#                     db.commit()

#                     #guest = session.query(users).filter_by(email=f'{form.email.data}').first()
#                     statement = sqlalchemy.text(f"SELECT * FROM users g WHERE g.email='{form.email.data}';")
#                     guest = db.execute(statement)
#                     db.commit()
#                     guest = generate_table_return_result(guest)
#                     guest = json.loads(guest)
                    
#                     flash('Your account has been updated! Please log in again.', 'success')
#                     return redirect(url_for('auth.login'))
#                 except Exception as e:
#                     db.rollback()
#                     return Response(str(e), 403)
#         if form.name.data != current_user.name:
#             statement = sqlalchemy.text(f"SELECT * FROM users u WHERE u.name='{form.name.data}';")
#             guest = db.execute(statement).fetchone()
#             db.commit()
#             if guest:
#                 guest = generate_table_return_result(guest)
#                 guest = json.loads(guest)
#                 flash('That name is taken. Please choose a different one.', category='error')
#                 return redirect(url_for('views.profile'))
#             else:
#                 try:
#                     statement = sqlalchemy.text(f"UPDATE users SET name = '{form.name.data}' WHERE email = '{current_user.email}';")       
#                     db.execute(statement)
#                     db.commit()

#                     statement = sqlalchemy.text(f"SELECT * FROM users g WHERE g.name='{form.name.data}';")
#                     guest = db.execute(statement)
#                     db.commit()
#                     guest = generate_table_return_result(guest)
#                     guest = json.loads(guest)

#                     flash('Your name has been updated! Please log in again.', 'success')
#                     return redirect(url_for('auth.login'))
#                 except Exception as e:
#                     db.rollback()
#                     return Response(str(e), 403)
#     return render_template('profile.html', title='Profile', form=form, user=current_user)

@views.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.email.data != current_user.email:
            statement = sqlalchemy.text(f"SELECT * FROM users u WHERE u.email='{form.email.data}';")
            guest = db.execute(statement).fetchone()
            db.commit()
            logging.warning(guest)
            if guest:
                flash('That email is taken. Please choose a different one.', category='error')
                return redirect(url_for('views.profile'))
        if form.name.data != current_user.name:
            statement = sqlalchemy.text(f"SELECT * FROM users u WHERE u.name='{form.name.data}';")
            guest = db.execute(statement).fetchone()
            db.commit()
            if guest:
                flash('That name is taken. Please choose a different one.', category='error')
                return redirect(url_for('views.profile'))    
        # if both new name and email are valid
        try:
            statement = sqlalchemy.text(f"UPDATE users SET email = '{form.email.data}', name = '{form.name.data}' WHERE email = '{current_user.email}';")       
            db.execute(statement)
            db.commit()
            flash('Your account has been updated! Please log in again.', 'success')
            return redirect(url_for('auth.logout'))
        except Exception as e:
            db.rollback()
            return Response(str(e), 403)
    return render_template('profile.html', title='Profile', form=form, user=current_user)

@views.route("/")
@views.route("/statistics", methods=["GET", "POST"])
@login_required
def statistics():
    form = StatsForm()
    data, data1, data2 = None, None, None
    if form.validate_on_submit():
        try:
            statement = sqlalchemy.text(f"SELECT property_id, COUNT(*) as count FROM bookings WHERE owner_email = '{form.email.data}' GROUP BY property_id HAVING COUNT(*) >= ALL (SELECT COUNT(*) FROM bookings WHERE owner_email = '{form.email.data}' GROUP BY property_id);")
            res = db.execute(statement)
            data = generate_table_return_result(res)
            data = json.loads(data)
            logging.warning(data)

            statement = sqlalchemy.text(f"SELECT neighbourhood, COUNT(*) as count FROM properties WHERE owner = '{form.email.data}' GROUP BY neighbourhood;")
            res = db.execute(statement)
            data1 = generate_table_return_result(res)
            data1 = json.loads(data1)

            statement = sqlalchemy.text(f"SELECT SUM(p.price_per_night*duration) FROM properties p, bookings b WHERE b.owner_email = p.owner AND p.property_id = b.property_id AND p.owner = '{form.email.data}';")
            res = db.execute(statement)
            data2 = generate_table_return_result(res)
            data2 = json.loads(data2)

        except Exception as e:
            db.rollback()
            return Response(str(e), 403)
    return render_template('statistics.html', title='Statistics', form=form, stats_data=data, stats_data1=data1, stats_data2=data2, user=current_user)



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