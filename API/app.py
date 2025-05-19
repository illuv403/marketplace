from difflib import get_close_matches
from itertools import product

from flask import Flask, render_template, redirect, url_for, request, session, flash
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
            session['cart'] = {}
            return redirect(url_for('index'))

        if request.method == 'POST':

            email = request.form['email']
            password = request.form['password']

            user = auth_service.login_user(email, password)

            if user:
                session.permanent = True
                auth_service.new_session(user)
                session['cart'] = {}
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password. Try again.')

        return render_template('author.html')

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':

            password = request.form['password']
            if auth_service.password_check(password):
                user = auth_service.register_user(
                    name=request.form['name'],
                    surname=request.form['surname'],
                    login=request.form['login'],
                    email=request.form['email'],
                    password= password
                )

                if user:
                    session.permanent = True
                    auth_service.new_session(user)
                    session['cart'] = {}
                    return redirect(url_for('index'))
            else:
                flash('Your password dont meet security conditions.'
                    ' At least 8 symbols.'
                    ' At least 1 lowercase letter.'
                    ' At least 1 uppercase letter.'
                    ' At least 1 digit.'
                    ' At least 1 special symbol.')

        return render_template('regist.html')

    @app.route('/logout', methods=['GET'])
    def logout():
        AuthService.end_session()
        return redirect(url_for('auth'))


    @app.route('/add_to_cart', methods=['POST'])
    def add_to_cart():
        if not AuthService.is_logged_in():
            return redirect(url_for('auth'))

        product_id = request.form.get('product_id')
        product_repo = ProductRepository(session=db_session)
        if product_id:
            cart = session.get('cart', {})
            if product_id not in cart and product_repo.get_product_by_id(product_id).quantity >= 1 :
                cart[product_id] = 1
            session['cart'] = cart
        return redirect(url_for('index', page=request.args.get('page', 1)))

    @app.route('/remove_from_cart', methods=['POST'])
    def remove_from_cart():
        if not AuthService.is_logged_in():
            return redirect(url_for('auth'))

        product_id = request.form.get('cart_product_id')

        if product_id:
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
        product_repo = ProductRepository(session=db_session)
        if product_id in cart:
            if action == 'inc':
                product = product_repo.get_product_by_id(product_id)
                if product.quantity >= cart[product_id] + 1 :
                    cart[product_id] += 1
                else:
                    flash('There is not that much in stock.', category=product_id)
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
        product_repo = ProductRepository(session=db_session)
        user = user_repo.get_user_by_id(user_id)

        cart_ids = session.get('cart', {})
        product_list = []
        for cart_id in cart_ids:
            product_list.append(page_service.get_products_from_cart_by_id(cart_id))
            product = product_repo.get_product_by_id(cart_id)
            product_repo.update_product(cart_id, None, None,None, product.quantity - cart_ids[cart_id], None)
        email_sending_service.send_email(user.email, product_list)

        session['cart'] = {}

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
        cart = session.get('cart', {})
        subtotal = 0

        cart_products = []
        for product_id in cart:
            product = page_service.get_products_from_cart_by_id(product_id)
            if product:
                cart_products.append(product)

        shipping = 5.00 if subtotal > 0 else 0
        tax = round(float(subtotal) * 0.07, 2)
        total = round(float(subtotal) + shipping + tax, 2)

        return render_template(
            'index.html',
            products=matched_products,
            page=1,
            total_pages=1,
            categories=categories,
            cart_products=cart_products,
            subtotal=subtotal,
            shipping=shipping,
            tax=tax,
            total=total,
            isSearch=True
        )

    @app.route('/search_by_cat', methods=['POST'])
    def search_by_cat():
        products_by_cats = []
        product_repo = ProductRepository(session=db_session)

        for category_name in request.form:
            products_by_cat = product_repo.get_product_by_category(category_name)
            if products_by_cat:
                for gotten_product in products_by_cat:
                    products_by_cats.append(gotten_product)

        categories = page_service.get_categories()
        cart = session.get('cart', {})
        subtotal = 0
        cart_products = []
        for product_id in cart:
            product = page_service.get_products_from_cart_by_id(product_id)
            if product:
                cart_products.append(product)

        shipping = 5.00 if subtotal > 0 else 0
        tax = round(float(subtotal) * 0.07, 2)
        total = round(float(subtotal) + shipping + tax, 2)

        return render_template(
            'index.html',
            products=products_by_cats,
            page=1,
            total_pages=1,
            categories=categories,
            cart_products=cart_products,
            subtotal=subtotal,
            shipping=shipping,
            tax=tax,
            total=total,
            isSearch=True
        )

    @app.route('/clear_cart', methods=['POST'])
    def clear_cart():
        session['cart'] = {}

        return redirect(url_for('index', page=request.args.get('page', 1)))

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app



