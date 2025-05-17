from difflib import get_close_matches

from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta

from API.services import email_sending_service
from API.services.auth_service import AuthService
from API.services.main_page_service import PageService
from DB.database import db_session, init_db
from DB.fill_db import FillProducts
from DB.repositories.product_repository import ProductRepository
from DB.repositories.user_repository import UserRepository

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

        cart = session.get('cart', {})
        cart_products = []
        subtotal = 0

        for product_id, quantity in cart.items():
            product = page_service.get_products_from_cart_by_id(product_id)
            if product:
                product.local_quantity = quantity
                cart_products.append(product)
                subtotal += product.price * quantity

        shipping = 5.00 if subtotal > 0 else 0
        tax = round(float(subtotal) * 0.07, 2)
        total = round(float(subtotal) + shipping + tax, 2)
        return render_template('index.html',
                               products=products,
                               page=page,
                               total_pages=page_service.total_pages,
                               categories=categories,
                               cart_products=cart_products,
                               subtotal=subtotal,
                               shipping=shipping,
                               tax=tax,
                               total=total)

    @app.route('/auth', methods=['GET', 'POST'])
    def auth():
        if AuthService.is_logged_in() and request.method == 'GET':
            products_in_cart = page_service.get_user_cart(session.get('user_id'))
            cart = {}
            for product_in_cart in products_in_cart:
                cart[str(product_in_cart.id)] = 1
            session['cart'] = cart
            return redirect(url_for('index'))

        if request.method == 'POST':

            email = request.form['email']
            password = request.form['password']

            user = auth_service.login_user(email, password)

            if user:
                session.permanent = True
                auth_service.new_session(user)
                products_in_cart = page_service.get_user_cart(user.id)
                cart = {}
                for product_in_cart in products_in_cart:
                    cart[str(product_in_cart.id)] = 1
                session['cart'] = cart
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
                cart = {}
                for product_in_cart in products_in_cart:
                    cart[str(product_in_cart.id)] = 1
                session['cart'] = cart
                return redirect(url_for('index'))

        return render_template('regist.html')

    @app.route('/logout', methods=['GET'])
    def logout():
        AuthService.end_session()
        return redirect(url_for('auth'))

    @app.route('/product}')
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
            cart = session.get('cart', {})
            if product_id not in cart:
                cart[product_id] = 1
            session['cart'] = cart
        return redirect(url_for('index', page=request.args.get('page', 1)))

    @app.route('/remove_from_cart', methods=['POST'])
    def remove_from_cart():
        if not AuthService.is_logged_in():
            return redirect(url_for('auth'))

        user_id = session.get('user_id')
        product_id = request.form.get('cart_product_id')

        if user_id and product_id:

            page_service.remove_product_from_cart(user_id=user_id, product_id=product_id)
            cart = session.get('cart', {})
            if product_id in cart:
                del cart[product_id]
            session['cart'] = cart

        return redirect(url_for('index', page=request.args.get('page', 1)))

    @app.route('/update_cart_product_quantity', methods=['POST'])
    def update_cart_product_quantity():
        product_id = request.form.get('product_id')
        action = request.form.get('action')

        cart = session.get('cart', {})

        if product_id in cart:
            if action == 'inc':
                cart[product_id] += 1
            elif action == 'dec':
                cart[product_id] = max(1, cart[product_id] - 1)

        session['cart'] = cart
        return redirect(url_for('index', page=request.args.get('page', 1)))

    @app.route('/checkout', methods=['POST'])
    def checkout():
        if not AuthService.is_logged_in():
            return redirect(url_for('auth'))

        user_id = session.get('user_id')
        user_repo = UserRepository(session=db_session)
        user = user_repo.get_user_by_id(user_id)

        cart_ids = session.get('cart', [])
        product_list = []
        for cart_id in cart_ids:
            product_list.append(page_service.get_products_from_cart_by_id(cart_id))

        email_sending_service.send_email(user.email, product_list)

        session['cart'] = []

        return redirect(url_for('index', page=request.args.get('page', 1)))

    @app.route('/search', methods=['GET'])
    def search():
        search_text = request.args.get('search_text', '')
        if not search_text:
            return redirect(url_for('index'))

        product_repo = ProductRepository(session=db_session)
        products = product_repo.get_all_products()

        product_names = []
        for product in products:
            product_names.append(product.name)

        matches = get_close_matches(search_text, product_names, cutoff=0.5)

        matched_products = []
        for product in products:
            if product.name in matches:
                matched_products.append(product)

        categories = page_service.get_categories()
        cart_product_ids = session.get('cart', [])

        cart_products = []
        for product_id in cart_product_ids:
            product = page_service.get_products_from_cart_by_id(product_id)
            cart_products.append(product)

        return render_template(
            'index.html',
            products=matched_products,
            page=1,
            total_pages=1,
            categories=categories,
            cart_products=cart_products
        )

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
