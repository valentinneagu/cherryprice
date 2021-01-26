import os
import json
import psycopg2

from dotenv import load_dotenv
load_dotenv()

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
HOST = ''
AUTHSECRET = 'secretbarosan'
EXPIRESSECONDS = 3000


def authenticate(client_id, client_secret):
    conn = None
    query = "select * from clients where \"ClientId\"='" + client_id + "' and \"ClientSecret\"='" + client_secret + "'"

    try:
        conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASSWORD, host=HOST)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        is_admin = False

        if cur.rowcount == 1:
            for row in rows:
                is_admin = row[3]
                payload = AuthPayload(row[0], row[1], is_admin)
                break

            encoded_jwt = jwt.encode(payload.__dict__, AUTHSECRET, algorithm='HS256')
            response = AuthResponse(encoded_jwt, EXPIRESSECONDS, is_admin)

            return response.__dict__
        else:
            return False

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()
        return False

    finally:
        if conn is not None:
            cur.close()
            conn.close()


def verify(token):
    try:
        is_blacklisted = check_blacklist(token)
        if is_blacklisted:
            return {"success": False}
        else:
            decoded = jwt.decode(token, AUTHSECRET, algorithms=['HS256'])
            return decoded
    except Exception as error:
        print(error)
        return {"success": False}


def create(client_id, client_secret, is_admin):
    conn = None
    query = "insert into clients (\"ClientId\", \"ClientSecret\", \"IsAdmin\") values(%s,%s,%s)"
    check_user_exists_query = "select * from clients where \"ClientId\"='" + client_id + "'"

    try:
        conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASSWORD, host=HOST)
        cur = conn.cursor()
        cur.execute(check_user_exists_query)
        result = cur.fetchone()
        if result is not None and result[0] is not 0:
            return "Username already in use"
        else:
            cur.execute(query, (client_id, client_secret, is_admin))
            conn.commit()
            return True

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()
        return False

    finally:
        if conn is not None:
            cur.close()
            conn.close()


def blacklist(token):
    conn = None
    query = "insert into blacklist (\"token\") values(\'" + token + "\')"
    try:
        conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASSWORD, host=HOST)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def check_blacklist(token):
    conn = None
    query = "select count(*) from blacklist where token=\'" + token + "\'"
    try:
        conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASSWORD, host=HOST)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result[0] == 1:
            return True
        else:
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return True
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def get_users():
    conn = None
    query = "select * from clients"
    try:
        conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASSWORD, host=HOST)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return True
    finally:
        if conn is not None:
            cur.close()
            conn.close()