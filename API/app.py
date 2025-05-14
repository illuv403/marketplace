from flask import Flask, render_template

from API.services.main_page_service import PageService
from DB.database import db_session, init_db
from DB.fill_db import FillProducts


def create_app():
    app = Flask(__name__, template_folder='templates')

    init_db()
    product_fill = FillProducts(db_session)
    product_fill.fill_all()

    @app.route("/")
    def index():
        page_service = PageService(session=db_session)
        products = page_service.get_random_products()
        return render_template('index.html' , products=products)

    @app.route('/auth', methods=['GET'])
    def auth():
        return render_template('author.html')

    @app.route('/product')
    def product():
        return render_template('seemore.html')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app