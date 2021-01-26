import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from cherryprice import app, db, bcrypt
from cherryprice.forms import RegistrationForm, LoginForm, UpdateAccountForm
from cherryprice.models import *
from flask_login import login_user, current_user, logout_user, login_required
import json
from flask import make_response
from datetime import datetime
from flask import request
import requests


AUTH_HOST = 'http://authservice:80'
SCRAPING_HOST = 'http://scrapingservice:80'


@app.route("/")
@app.route("/home")
def home():
    return "works"


@app.route("/getAllUsers", methods=["GET"])
def get_users():
    r = requests.get(AUTH_HOST + '/getAllUsers', verify=False)
    return r.text


@app.route("/register", methods=["POST", "DELETE"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    data = {'client_id': username, 'client_secret': password}
    r = requests.post(AUTH_HOST + '/client', data=data)
    return r.text


@app.route('/login', methods=["POST"])
def login():
    """
    If credentials are valid:
    {
        "token": "some_string"
        "expires_in": int
    }
    else
    {
        "success": false
    }
    :return: json
    """
    username = request.form.get("username")
    password = request.form.get("password")
    data = {'client_id': username, 'client_secret': password}
    r = requests.post(AUTH_HOST + '/auth', data=data)
    return r.text


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    authorization_header = request.headers.get('authorization')
    r = verify(authorization_header)
    r = json.loads(r.text)
    if 'clientId' in r.keys():
        watchlists = Watchlist.query.filter_by(user_id=r['id']).all()
        payload = {}
        for item in watchlists:
            payload[item.id] = item.name
        payload = json.dumps(payload)
        return make_response(payload)
    else:
        return make_response("404")


def verify(authorization_header):
    """
    should be used everytime an user wants resources
    If jwt is valid:
    {
        "clientId":"admin",
        "exp":1611602525,
        "id":7,
        "isAdmin":true
    }
    else
    {
        "success":false
    }
    :return:
    """
    r = requests.post(AUTH_HOST + '/verify', headers={'authorization': authorization_header})
    return r


@app.route("/price", methods=["POST"])
def get_price():
    url = request.form.get("url")
    r = requests.post(SCRAPING_HOST + '/price', data={'url': url})
    return r.text


# @app.route("/watchlist", methods=['GET', 'POST'])
# def dashboard():
#     watchlists = Watchlist.query.filter_by(user_id='1').all()
#     payload = {}
#     for item in watchlists:
#         payload[item.id] = item.name
#     payload = json.dumps(payload)
#     return make_response(payload)



# @app.route("/about")
# def about():
#     return render_template('about.html', title='About')


# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)
#
#
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)
#
#
# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('home'))


# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
#
#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)
#
#     return picture_fn
#
#
# @app.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_file = save_picture(form.picture.data)
#             current_user.image_file = picture_file
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Your account has been updated!', 'success')
#         return redirect(url_for('account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
#     return render_template('account.html', title='Account',
#                            image_file=image_file, form=form)
