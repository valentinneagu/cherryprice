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
    """
        If user does not exist:
        {'register': True}
        else if user exists:
        {'register': Username already exists}
        else:
        {'register': False
        :return: json
        """
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
        "login": false
    }
    :return: json
    """
    username = request.form.get("username")
    password = request.form.get("password")
    data = {'client_id': username, 'client_secret': password}
    r = requests.post(AUTH_HOST + '/auth', data=data)
    return r.text


@app.route('/logout', methods=["POST"])
def logout():
    """
    If token is valid:
        {'logout': True}
    else:
        {'logout': False}
    :return: json
    """
    authorization_header = request.headers.get('authorization')
    r = requests.post(AUTH_HOST + '/logout', headers={'authorization': authorization_header})
    return r


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    authorization_header = request.headers.get('authorization')
    r = verify(authorization_header)
    r = json.loads(r.text)
    if 'clientId' in r.keys():
        watchlists = Watchlist.query.filter_by(user_id=r['id']).all()
        payload = []
        for item in watchlists:
            # payload[item.id] = item.name
            d = {'id': item.id, 'name': item.name}
            payload.append(d)
        payload = json.dumps(payload)
        return make_response(payload)
    else:
        return make_response("404")


@app.route("/watchlist", methods=['POST'])
def watchlist():
    authorization_header = request.headers.get('authorization')
    r = verify(authorization_header)
    r = json.loads(r.text)
    if 'clientId' in r.keys():
        watchlist = request.form.get("watchlist")
        watchlistsbridges = Watchlistbridge.query.filter_by(watchlist_id=watchlist).all()
        for item in watchlistsbridges:
            product = Product.query.filter_by(link=item.product_link).first()
            d = {'name': product.name, 'link': product.link, 'price': product.price}
            payload.append(d)
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


# @app.route("/price", methods=["POST"])
def get_price(url):
    # url = request.form.get("url")
    r = requests.post(SCRAPING_HOST + '/price', data={'url': url})
    r = json.loads(r.text)
    return float(r['price'].replace(',', '.'))


@app.route("/test_price", methods=["POST"])
def test_price():
    url = request.form.get("url")
    r = requests.post(SCRAPING_HOST + '/price', data={'url': url})
    # r = float(r.text[0]["price"].replace(',','.'))
    r = json.loads(r.text)
    return r['price'].replace(',', '.')


@app.route("/product", methods=['POST'])
def product():
    authorization_header = request.headers.get('authorization')
    r = verify(authorization_header)
    r = json.loads(r.text)
    if 'clientId' in r.keys():
        product_link = request.form.get("product_link")
        product_history = Product.query.filter_by(link=product_link).all()
        payload = []
        for item in product_history:
            payload[str(item.date_queried)] = item.price
        payload = json.dumps(payload)
        return make_response(payload)
    else:
        return make_response("404")


@app.route("/deleteproductfromwatchlist", methods=['POST'])
def delete_product_from_watchlist():
    authorization_header = request.headers.get('authorization')
    r = verify(authorization_header)
    r = json.loads(r.text)
    if 'clientId' in r.keys():
        product_link = request.form.get("product_link")
        watchlistid = request.form.get("watchlist_id")
        product = Watchlistbridge.query.filter_by(product_link=product_link, watchlist_id=watchlistid).first()
        db.session.delete(product)
        db.session.commit()
        return make_response("Success")
    else:
        return make_response("404")


@app.route("/deletewatchlist", methods=['POST'])
def delete_watchlist():
    authorization_header = request.headers.get('authorization')
    r = verify(authorization_header)
    r = json.loads(r.text)
    if 'clientId' in r.keys():
        watchlistid = request.form.get("watchlist_id")
        watchlist = Watchlist.query.filter_by(id=watchlistid).first()
        bridges = Watchlistbridge.query.filter_by(watchlist_id=watchlistid).all()
        for item in bridges:
            db.session.delete(item)
        db.session.delete(watchlist)
        db.session.commit()
        return make_response("Success")
    else:
        return make_response("404")


@app.route("/addwatchlist", methods=['POST'])
def add_watchlist():
    authorization_header = request.headers.get('authorization')
    r = verify(authorization_header)
    r = json.loads(r.text)
    if 'clientId' in r.keys():
        watchlistname = request.form.get("watchlist_name")
        new_watchlist = Watchlist(user_id=r['id'], name=watchlistname)
        db.session.add(new_watchlist)
        db.session.commit()
        return make_response("Success")
    else:
        return make_response("404")


@app.route("/addproduct", methods=['POST'])
def add_product():
    authorization_header = request.headers.get('authorization')
    r = verify(authorization_header)
    r = json.loads(r.text)
    if 'clientId' in r.keys():
        product_name = request.form.get("product_name")
        product_link = request.form.get("product_link")
        watchlist_id = request.form.get("watchlist_id")
        product_price = get_price(product_link)
        new_product = Product(name=product_name, link=product_link, price=product_price)
        new_bridge = Watchlistbridge(watchlist_id=watchlist_id, product_link=product_link)
        db.session.add(new_product)
        db.session.add(new_bridge)
        db.session.commit()
        return make_response("Success")
    else:
        return make_response("404")
