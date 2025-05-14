from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta

from API.services.auth_service import AuthService
from API.services.main_page_service import PageService
from DB.database import db_session, init_db
from DB.fill_db import FillProducts


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'gnlrjjnarvnioernviloergvrvsd;vlckmasl;kdv'
    app.permanent_session_lifetime = timedelta(minutes=15)

    init_db()
    product_fill = FillProducts(db_session)
    product_fill.fill_all()

    @app.route("/")
    def index():
        page_service = PageService(session=db_session)
        products = page_service.get_random_products()
        return render_template('index.html' , products=products)

    @app.route('/auth', methods=['GET', 'POST'])
    def auth():
        auth_service = AuthService(session=db_session)

        if AuthService.is_logged_in() and request.method == 'GET':
            return redirect(url_for('index'))

        if request.method == 'POST':
            action = request.form.get('action', 'login')

            if action == 'register':
                user = auth_service.register_user(
                    name=request.form['name'],
                    surname=request.form['surname'],
                    login=request.form['login'],
                    email=request.form['email'],
                    password=request.form['password']
                )

                if user:
                    session.permanent = True
                    auth_service.new_session(user)
                    return redirect(url_for('index'))
            elif action == 'login':
                email = request.form['email']
                password = request.form['password']

                user = auth_service.login_user(email, password)

                if user:
                    session.permanent = True
                    auth_service.new_session(user)
                    return redirect(url_for('index'))

        return render_template('author.html')

    @app.route('/logout', methods=['GET'])
    def logout():
        AuthService.end_session()
        return redirect(url_for('auth'))

    @app.route('/product')
    def product():
        return render_template('seemore.html')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app