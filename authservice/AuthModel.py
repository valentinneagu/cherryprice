import os
import json
import psycopg2
from __init__ import *
from dotenv import load_dotenv
from flask import make_response

load_dotenv()
from models import *
import jwt
from AuthPayload import AuthPayload
from AuthResponse import AuthResponse

# Get environment variables
# DBNAME = os.getenv('DBNAME')
# DBUSER = os.getenv('DBUSER')
# DBPASSWORD = os.getenv("DBPASSWORD")
# AUTHSECRET = os.getenv("AUTHSECRET")
# EXPIRESSECONDS = os.getenv('EXPIRESSECONDS')

DBNAME = 'postgres'
DBUSER = 'auth'
DBPASSWORD = 'auth'
HOST = 'https://db'
AUTHSECRET = 'secretbarosan'
EXPIRESSECONDS = 3000
PORT = 5432


def authenticate(client_id, client_secret):
    user = User.query.filter_by(username=client_id).first()

    if user and bcrypt.check_password_hash(user.password, client_secret):
        payload = AuthPayload(user.id, user.username)
        encoded_jwt = jwt.encode(payload.__dict__, AUTHSECRET, algorithm='HS256')
        response = AuthResponse(encoded_jwt, EXPIRESSECONDS)
        return response.__dict__
    else:
        return False


def verify(token):
    try:
        is_blacklisted = check_blacklist(token)
        if is_blacklisted:
            return {"verify": False}
        else:
            decoded = jwt.decode(token, AUTHSECRET, algorithms=['HS256'])
            # username = json.loads(decoded)['clientId']
            # app.logger.error('ID {}'
            #                  .format(username))
            # user = User.query.filter_by(username=username).first()
            # if user:
            return decoded
            # else:
            #     return {"verify": False}
    except Exception as error:
        print(error)
        return {"verify": False}


def create(client_id, client_secret):
    hashed_password = bcrypt.generate_password_hash(client_secret).decode('utf-8')
    user = User(username=client_id, password=hashed_password)
    user_exists = User.query.filter_by(username=client_id).first()

    if user_exists is None:
        db.session.add(user)
        db.session.commit()
        return True
    else:
        return "Username already exists"


def blacklist(token):
    blacklist_element = Blacklist(token)
    already_blacklisted = Blacklist.query.filter_by(token=token).first()

    if already_blacklisted is None:
        db.session.add(blacklist_element)
        db.session.commit()
        return True
    else:
        return False


def check_blacklist(token):
    blacklisted = Blacklist.query.filter_by(token=token).first()

    if blacklisted:
        return True
    else:
        return False


def get_users():
    users = User.query.all()
    payload = {}
    for item in users:
        payload[item.id] = item.username
    payload = json.dumps(payload)
    return make_response(payload)
