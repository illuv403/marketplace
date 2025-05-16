from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta

from API.services.auth_service import AuthService
from API.services.main_page_service import PageService
from DB.database import db_session, init_db
from DB.fill_db import FillProducts

from secret_key import secret_key


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = secret_key
    app.permanent_session_lifetime = timedelta(minutes=15)

    init_db()
    product_fill = FillProducts(db_session)
    product_fill.fill_all()
    page_service = PageService(session=db_session)
    auth_service = AuthService(session=db_session)

    @app.route("/")
    def index():
        page = request.args.get("page", 1, int)
        products = page_service.get_random_products(page)
        categories = page_service.get_categories()

        cart_product_ids = session.get('cart', [])
        cart_products = [page_service.get_products_from_cart_by_id(product_id) for product_id in cart_product_ids]
        return render_template('index.html', products=products, page=page, total_pages=page_service.total_pages,
                               categories=categories, cart_products=cart_products)

    @app.route('/auth', methods=['GET', 'POST'])
    def auth():
        if AuthService.is_logged_in() and request.method == 'GET':
            products_in_cart = page_service.get_user_cart(session.get('user_id'))
            session['cart'] = [product_in_cart.id for product_in_cart in products_in_cart]
            return redirect(url_for('index'))

        if request.method == 'POST':

            email = request.form['email']
            password = request.form['password']

            user = auth_service.login_user(email, password)

            if user:
                session.permanent = True
                auth_service.new_session(user)
                products_in_cart = page_service.get_user_cart(user.id)
                session['cart'] = [product_in_cart.id for product_in_cart in products_in_cart]
                return redirect(url_for('index'))

        return render_template('author.html')

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':

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
                products_in_cart = page_service.get_user_cart(user.id)
                session['cart'] = [product_in_cart.id for product_in_cart in products_in_cart]
                return redirect(url_for('index'))

        return render_template('regist.html')

    @app.route('/logout', methods=['GET'])
    def logout():
        AuthService.end_session()
        return redirect(url_for('auth'))

    @app.route('/product')
    def product():
        return render_template('seemore.html')


    @app.route('/add_to_cart', methods=['POST'])
    def add_to_cart():
        if not AuthService.is_logged_in():
            return redirect(url_for('auth'))

        user_id = session.get('user_id')
        product_id = request.form.get('product_id')

        if user_id and product_id:
            page_service.add_product_to_cart(user_id=user_id, product_id=product_id)
            session['cart'] = [p.id for p in page_service.get_user_cart(user_id)]

        return redirect(url_for('index', page=request.args.get('page', 1)))

    @app.route('/remove_from_cart', methods=['POST'])
    def remove_from_cart():
        if not AuthService.is_logged_in():
            return redirect(url_for('auth'))

        user_id = session.get('user_id')
        product_id = request.form.get('cart_product_id')

        if user_id and product_id:
            page_service.remove_product_from_cart(user_id=user_id, product_id=product_id)
            session['cart'] = [p.id for p in page_service.get_user_cart(user_id)]

        return redirect(url_for('index', page=request.args.get('page', 1)))

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
