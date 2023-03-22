# ? Cross-origin Resource Sharing - here it allows the view and core applications deployed on different ports to communicate. No need to know anything about it since it's only used once
from flask_cors import CORS, cross_origin
# ? Python's built-in library for JSON operations. Here, is used to convert JSON strings into Python dictionaries and vice-versa
import json
# ? flask - library used to write REST API endpoints (functions in simple words) to communicate with the client (view) application's interactions
# ? request - is the default object used in the flask endpoints to get data from the requests
# ? Response - is the default HTTP Response object, defining the format of the returned data by this api
from flask import Flask, request, Response
# ? sqlalchemy is the main library we'll use here to interact with PostgresQL DBMS
import sqlalchemy
# ? Just a class to help while coding by suggesting methods etc. Can be totally removed if wanted, no change
from typing import Dict


# ? web-based applications written in flask are simply called apps are initialized in this format from the Flask base class. You may see the contents of `__name__` by hovering on it while debugging if you're curious
app = Flask(__name__)

# ? Just enabling the flask app to be able to communicate with any request source
CORS(app)

# ? building our `engine` object from a custom configuration string
# ? for this project, we'll use the default postgres user, on a database called `postgres` deployed on the same machine
YOUR_POSTGRES_PASSWORD = "postgres"
connection_string = f"postgresql://postgres:{YOUR_POSTGRES_PASSWORD}@localhost/postgres"
engine = sqlalchemy.create_engine(
    "postgresql://postgres:postgres@localhost/postgres"
)

# ? `db` - the database (connection) object will be used for executing queries on the connected database named `postgres` in our deployed Postgres DBMS
db = engine.connect()

# ? A dictionary containing
data_types = {
    'boolean': 'BOOL',
    'integer': 'INT',
    'text': 'TEXT',
    'time': 'TIME',
}



# guest's bookings page
@app.get("/mybookings")
def get_relation():
    # ? This method returns the contents of a table whose name (table-name) is given in the url `http://localhost:port/mybookings?name=bookings&email=blabla`
    # ? Below is the default way of parsing the arguments from http url's using flask's request object
    relation_name = request.args.get('name', default="", type=str)
    email_name = request.args.get('email', default="", type=str)
    # ? We use try-except statements for exception handling since any wrong query will crash the whole flow
    try:
        # ? Statements are built using f-strings - Python's formatted strings
        # ! Use cursors for better results
        statement = sqlalchemy.text(f"SELECT * FROM {relation_name} b WHERE b.guest_email == {email_name} AND b.end_date >= SELECT NOW() ORDER BY b.start_date;")
        # ? Results returned by the DBMS after execution are stored into res object defined in sqlalchemy (for reference)
        res = db.execute(statement)
        # ? committing the statement writes the db state to the disk; note that we use the concept of rollbacks for safe DB management
        db.commit()
        # ? Data is extracted from the res objects by the custom function for each query case
        # ! Note that you'll have to write custom handling methods for your custom queries
        data = generate_table_return_result(res)
        # ? Response object is instantiated with the formatted data and returned with the success code 200
        return Response(data, 200)
    except Exception as e:
        # ? We're rolling back at any case of failure
        db.rollback()
        # ? At any error case, the error is returned with the code 403, meaning invalid request
        # * You may customize it for different exception types, in case you may want
        return Response(str(e), 403)

# owner's listings page
@app.get("/mylistings")
def get_relation():
    # ? This method returns the contents of a table whose name (table-name) is given in the url `http://localhost:port/mylistings?name=listings`
    # ? Below is the default way of parsing the arguments from http url's using flask's request object
    relation_name = request.args.get('name', default="", type=str)
    email_name = request.args.get('email', default="", type=str)
    # ? We use try-except statements for exception handling since any wrong query will crash the whole flow
    try:
        # ? Statements are built using f-strings - Python's formatted strings
        # ! Use cursors for better results
        statement = sqlalchemy.text(f"SELECT * FROM {relation_name} l WHERE l.guest_email == {email_name};")
        # ? Results returned by the DBMS after execution are stored into res object defined in sqlalchemy (for reference)
        res = db.execute(statement)
        # ? committing the statement writes the db state to the disk; note that we use the concept of rollbacks for safe DB management
        db.commit()
        # ? Data is extracted from the res objects by the custom function for each query case
        # ! Note that you'll have to write custom handling methods for your custom queries
        data = generate_table_return_result(res)
        # ? Response object is instantiated with the formatted data and returned with the success code 200
        return Response(data, 200)
    except Exception as e:
        # ? We're rolling back at any case of failure
        db.rollback()
        # ? At any error case, the error is returned with the code 403, meaning invalid request
        # * You may customize it for different exception types, in case you may want
        return Response(str(e), 403)
    
# whole listings page
@app.get("/listings")
def get_relation():
    # ? This method returns the contents of a table whose name (table-name) is given in the url `http://localhost:port/listings?name=listings`
    # ? Below is the default way of parsing the arguments from http url's using flask's request object
    relation_name = request.args.get('name', default="", type=str)
    # ? We use try-except statements for exception handling since any wrong query will crash the whole flow
    try:
        # ? Statements are built using f-strings - Python's formatted strings
        # ! Use cursors for better results
        statement = sqlalchemy.text(f"SELECT * FROM {relation_name};")
        # ? Results returned by the DBMS after execution are stored into res object defined in sqlalchemy (for reference)
        res = db.execute(statement)
        # ? committing the statement writes the db state to the disk; note that we use the concept of rollbacks for safe DB management
        db.commit()
        # ? Data is extracted from the res objects by the custom function for each query case
        # ! Note that you'll have to write custom handling methods for your custom queries
        data = generate_table_return_result(res)
        # ? Response object is instantiated with the formatted data and returned with the success code 200
        return Response(data, 200)
    except Exception as e:
        # ? We're rolling back at any case of failure
        db.rollback()
        # ? At any error case, the error is returned with the code 403, meaning invalid request
        # * You may customize it for different exception types, in case you may want
        return Response(str(e), 403)


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
    return json.dumps(output)


# ? This method can be used by waitress-serve CLI 
def create_app():
   return app

# ? The port where the debuggable DB management API is served
PORT = 2222
# ? Running the flask app on the localhost/0.0.0.0, port 2222
# ? Note that you may change the port, then update it in the view application too to make it work (don't if you don't have another application occupying it)
if __name__ == "__main__":
    app.run("0.0.0.0", PORT)
    # ? Uncomment the below lines and comment the above lines below `if __name__ == "__main__":` in order to run on the production server
    # ? Note that you may have to install waitress running `pip install waitress`
    # ? If you are willing to use waitress-serve command, please add `/home/sadm/.local/bin` to your ~/.bashrc
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=PORT)