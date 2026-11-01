
import os
import re
import sqlite3
import logging
from datetime import datetime, timedelta, timezone
from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("Set the SECRET_KEY environment variable.")

DATABASE = os.environ.get("DATABASE_PATH", "password_security.db")
MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 5

logging.basicConfig(
    filename="security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                failed_attempts INTEGER DEFAULT 0,
                lockout_until TEXT
            )
        """)

def valid_password(password):
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"[0-9]", password)
        and re.search(r"[^A-Za-z0-9]", password)
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or len(username) > 50:
        flash("Enter a valid username.")
        return redirect(url_for("home"))

    if not valid_password(password):
        flash("Password must have 8 characters, uppercase, lowercase, a number and a special character.")
        return redirect(url_for("home"))

    password_hash = generate_password_hash(password)

    try:
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )

        logging.info("Registration successful: %s", username)
        flash("Registration successful!")

    except sqlite3.IntegrityError:
        flash("Username already exists.")

    return redirect(url_for("home"))

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    with get_connection() as connection:
        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if user is None:
            logging.warning("Failed login for unknown username")
            flash("Invalid username or password.")
            return redirect(url_for("home"))

        now = datetime.now(timezone.utc)

        if user["lockout_until"]:
            unlock_time = datetime.fromisoformat(user["lockout_until"])

            if now < unlock_time:
                flash("Account temporarily locked.")
                return redirect(url_for("home"))

            connection.execute(
                "UPDATE users SET failed_attempts = 0, lockout_until = NULL WHERE id = ?",
                (user["id"],)
            )

        if check_password_hash(user["password_hash"], password):
            connection.execute(
                "UPDATE users SET failed_attempts = 0, lockout_until = NULL WHERE id = ?",
                (user["id"],)
            )

            session.clear()
            session["username"] = username

            logging.info("Successful login: %s", username)
            flash("Login successful!")

        else:
            attempts = user["failed_attempts"] + 1
            lockout = None

            if attempts >= MAX_ATTEMPTS:
                lockout = (
                    now + timedelta(minutes=LOCKOUT_MINUTES)
                ).isoformat()

            connection.execute(
                "UPDATE users SET failed_attempts = ?, lockout_until = ? WHERE id = ?",
                (attempts, lockout, user["id"])
            )

            logging.warning("Failed login: %s", username)

            if lockout:
                logging.warning("Account locked: %s", username)
                flash("Account locked for 5 minutes.")
            else:
                flash("Invalid username or password.")

    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have logged out.")
    return redirect(url_for("home"))

@app.route("/health")
def health():
    return {"status": "ok"}

initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
