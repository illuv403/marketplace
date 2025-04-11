from flask import Flask
from DB.database import db_session, init_db

def create_app():
    app = Flask(__name__)

    init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
