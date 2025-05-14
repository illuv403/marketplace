from flask import Flask, render_template
from DB.database import db_session, init_db

def create_app():
    app = Flask(__name__, template_folder='templates')

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/auth", methods=['GET', 'POST'])
    def auth():
        return render_template('author.html')

    @app.route('/product')
    def product():
        return render_template('seemore.html')

    init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app