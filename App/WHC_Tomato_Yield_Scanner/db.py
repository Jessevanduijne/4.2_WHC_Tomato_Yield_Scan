import sqlite3
import click

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

def insertResult(files, result):
    db = get_db()
    db.execute(
        "INSERT INTO results (unique_id, session_id, files, val, percent_healthy) VALUES (?, ?, ?, ?, ?)",
        (helpers.generateRandomString(20), session.get("id"), files.tostring(), result.tostring(), (result>current_app.config["TOMATO_HEALTHY_PERCENTAGE"]).sum())
    )
    db.commit()