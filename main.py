import os
import sqlite3

try:
    import mysql.connector
except ModuleNotFoundError:
    mysql = None
else:
    mysql = mysql.connector

from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        city TEXT NOT NULL,
        country TEXT NOT NULL,
        occupation TEXT NOT NULL,
        hobby TEXT NOT NULL,
        programming_language TEXT NOT NULL,
        online_hours INTEGER NOT NULL,
        entertainment TEXT NOT NULL
    )
"""


def get_db_kind(connection):
    return "sqlite" if isinstance(connection, sqlite3.Connection) else "mysql"


def get_db_connection():
    if mysql is not None:
        try:
            return mysql.connect(
                host=os.environ.get("MYSQL_HOST", "localhost"),
                user=os.environ.get("MYSQL_USER", "root"),
                password=os.environ.get("MYSQL_PASSWORD", "Tasnim09!#"),
                database=os.environ.get("MYSQL_DATABASE", "sys"),
                autocommit=False,
            )
        except mysql.Error:
            print("MySQL unavailable; falling back to local SQLite database.")

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()
    db_kind = get_db_kind(connection)
    table_sql = CREATE_USERS_TABLE
    if db_kind == "mysql":
        table_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age INT NOT NULL,
                city VARCHAR(255) NOT NULL,
                country VARCHAR(255) NOT NULL,
                occupation VARCHAR(255) NOT NULL,
                hobby VARCHAR(255) NOT NULL,
                programming_language VARCHAR(255) NOT NULL,
                online_hours INT NOT NULL,
                entertainment VARCHAR(255) NOT NULL
            )
        """

    cursor = connection.cursor()
    cursor.execute(table_sql)
    connection.commit()
    cursor.close()
    connection.close()


initialize_database()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/submit-form", methods=["POST"])
def submit_form():
    full_name = (request.form.get("full_name") or "").strip()
    email = (request.form.get("email") or "").strip()
    city = (request.form.get("city") or "").strip()
    country = (request.form.get("country") or "").strip()
    occupation = (request.form.get("occupation") or "").strip()
    hobby = (request.form.get("hobby") or "").strip()
    programming_language = (request.form.get("programming_language") or "").strip()
    entertainment = (request.form.get("entertainment") or "").strip()

    try:
        age = int(request.form.get("age") or 0)
        online_hours = int(request.form.get("online_hours") or 0)
    except ValueError:
        return render_template("form.html", error="Age and online hours must be valid numbers.")

    if not all(
        [
            full_name,
            email,
            city,
            country,
            occupation,
            hobby,
            programming_language,
            entertainment,
        ]
    ) or age <= 0 or online_hours < 0:
        return render_template("form.html", error="Please complete all required fields correctly.")

    connection = get_db_connection()
    db_kind = get_db_kind(connection)
    placeholder = "%s" if db_kind == "mysql" else "?"
    query = f"""
        INSERT INTO users
        (full_name, email, age, city, country, occupation,
         hobby, programming_language, online_hours, entertainment)
        VALUES ({', '.join([placeholder] * 10)})
    """
    cursor = connection.cursor()

    try:
        cursor.execute(
            query,
            (
                full_name,
                email,
                age,
                city,
                country,
                occupation,
                hobby,
                programming_language,
                online_hours,
                entertainment,
            ),
        )
        connection.commit()
    except Exception as exc:
        return render_template("form.html", error=f"Could not save data: {exc}")
    finally:
        cursor.close()
        connection.close()

    return render_template("success.html", full_name=full_name)


@app.route("/users")
def users():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        columns = [column[0] for column in (cursor.description or [])]
        user_list = [dict(zip(columns, row)) for row in rows]
    finally:
        cursor.close()
        connection.close()

    return render_template("users.html", users=user_list)


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")