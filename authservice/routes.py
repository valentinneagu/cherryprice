from flask import Flask, request
import json
import hashlib
import AuthModel
from __init__ import *


@app.route('/')
def hello_world():
    app.logger.info("CE ZCETI MA?")
    return 'Hello Motherfuckers v2!'


@app.route("/client", methods=["POST", "DELETE"])
def client():
    if request.method == 'POST':

        # verify the token
        # TO do after we create first credentials

        # get the client_id and secret from the client application
        client_id = request.form.get("client_id")

        client_secret_input = request.form.get("client_secret")
        # is_admin = request.form.get("is_admin")

        app.logger.error('ID {} PASS {} FORM {}'
                         .format(client_id, client_secret_input, request.form))

        # the client secret in the database is "hashed" with a one-way hash
        # hash_object = hashlib.sha1(bytes(client_secret_input, 'utf-8'))
        # hashed_client_secret = hash_object.hexdigest()

        # make a call to the model to authenticate
        create_response = AuthModel.create(client_id, client_secret_input)
        return {'success': create_response}

    elif request.method == 'DELETE':
        # not yet implemented
        return {'success': False}
    else:
        return {'success': False}


# API Route for checking the client_id and client_secret
@app.route("/auth", methods=["POST"])
def auth():
    # get the client_id and secret from the client application
    client_id = request.form.get("client_id")
    client_secret = request.form.get("client_secret")

    # the client secret in the database is "hashed" with a one-way hash
    # hash_object = hashlib.sha1(bytes(client_secret_input, 'utf-8'))
    # hashed_client_secret = hash_object.hexdigest()

    # make a call to the model to authenticate
    authentication = AuthModel.authenticate(client_id, client_secret)
    if not authentication:
        return {'login': False}
    else:
        return json.dumps(authentication)


# API route for verifying the token passed by API calls
@app.route("/verify", methods=["POST"])
def verify():
    # verify the token
    authorization_header = request.headers.get('authorization')
    token = authorization_header.replace("Bearer ","")
    verification = AuthModel.verify(token)
    return verification


@app.route("/logout", methods=["POST"])
def logout():
    token = request.form.get("token")
    status = AuthModel.blacklist(token)
    return {'success': status}


@app.route("/getAllUsers", methods=["GET"])
def get_all_users():
    result = AuthModel.get_users()
    if result is None:
        return {'users': 'failed'}
    else:
        return result


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
