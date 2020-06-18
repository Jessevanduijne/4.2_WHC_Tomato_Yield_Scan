import sqlite3
import click
import numpy as np
import datetime

from flask import current_app, g, session
from flask.cli import with_appcontext

from . import helpers

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db():
    if "db" not in g:
        # If your linter gives an error here about sqlite3, it is safe to ignore
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e = None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
        
@click.command("init-db")
@with_appcontext
def init_db_command():
    # Clear the existing data and create new tables.
    click.echo("Initializing the database...")
    init_db()

def getResult(unique_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM results WHERE unique_id = ?",
        (unique_id,)
    ).fetchone()

def getResults(session_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM results WHERE session_id = ? LIMIT 10",
        (session_id,)
    ).fetchall()

def insertResult(files, values):
    unique_id = helpers.generateRandomString(20)

    db = get_db()
    db.execute(
        "INSERT INTO results (unique_id, session_id, files_dtype, files, val, percent_healthy, result_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (unique_id, session.get("id"), files.dtype.str, files.tostring(), values.tostring(), helpers.calculateHealthyPercentage(values), datetime.datetime.now())
    )
    db.commit()

    return unique_id