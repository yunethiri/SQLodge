import json
from flask import Flask, request, Response
import sqlalchemy
from typing import Dict
import sqlalchemy_utils as sql_utils
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

engine = sqlalchemy.create_engine(
    "postgresql://postgres:postgres@localhost/postgres"
)

connection = engine.connect()


@app.get("/table")
def get_table():
    table_name = request.args.get('name', default="", type=str)
    try:
        statement = f"SELECT * FROM {table_name};"
        res = connection.execute(statement)
        data = generate_table_return_result(res)
        return Response(data, 200)
    except Exception as e:
        return Response(str(e), 403)


@app.post("/table-create")
def create_table():
    data = request.data.decode()
    try:
        table = json.loads(data)
        statement = generate_create_table_statement(table)
        connection.execute(statement)
        return Response(statement, 200)
    except Exception as e:
        return Response(str(e), 403)


@app.post("/table-insert")
def insert_into_table():
    data = request.data.decode()
    try:
        insertion = json.loads(data)
        statement = generate_insert_table_statement(insertion)
        connection.execute(statement)
        return Response(statement, 200)
    except Exception as e:
        return Response(str(e), 403)


@app.post("/table-update")
def update_table():
    data = request.data.decode()
    try:
        update = json.loads(data)
        statement = generate_update_table_statement(update)
        connection.execute(statement)
        return Response(statement, 200)
    except Exception as e:
        return Response(str(e), 403)


@app.post("/table-delete")
def delete_row():
    data = request.data.decode()
    try:
        delete = json.loads(data)
        statement = generate_delete_statement(delete)
        connection.execute(statement)
        return Response(statement, 200)
    except Exception as e:
        return Response(str(e), 403)


def generate_table_return_result(res: sqlalchemy.engine.cursor.LegacyCursorResult):
    rows = []

    columns = list(res.keys())

    for row_number, row in enumerate(res):
        rows.append({})
        for column_number, value in enumerate(row):
            rows[row_number][columns[column_number]] = value
    output = {}
    output["columns"] = columns
    output["rows"] = rows
    return json.dumps(output)


def generate_delete_statement(details: Dict):
    table_name = details["name"]
    id = details["id"]
    statement = f"DELETE FROM {table_name} WHERE {table_name}.id={id};"
    return statement


def generate_update_table_statement(update: Dict):
    table_name = update["name"]
    id = update["id"]
    body = update["body"]
    statement = f"UPDATE {table_name} SET "
    for key, value in body.items():
        statement += f"{key}=\'{value}\',"
    statement = statement[:-1]+f" WHERE {table_name}.id={id};"
    return statement


def generate_insert_table_statement(insertion: Dict):
    table_name = insertion["name"]
    body = insertion["body"]
    statement = f"INSERT INTO {table_name}  "
    column_names = "("
    column_values = "("
    for key, value in body.items():
        column_names += (key+",")
        column_values += (f"\'{value}\',")
    column_names = column_names[:-1]+")"
    column_values = column_values[:-1]+")"
    statement = statement + column_names+" VALUES "+column_values+";"
    return statement


def generate_create_table_statement(table: Dict):
    table_body = table["body"]
    table_name = table["name"]
    statement = f"DROP TABLE IF EXISTS {table_name}; CREATE TABLE {table_name} (id serial NOT NULL PRIMARY KEY,"
    for key, value in table_body.items():
        statement += (key+" "+value+",")
    statement = statement[:-1] + ");"
    return statement


if __name__ == "__main__":
    app.run("0.0.0.0", 2222)
