from datetime import datetime
from datetime import timedelta
import os


class AuthPayload(dict):

    def __init__(self, id, client_id):
        super().__init__()
        expires_seconds = 3000

        # set the id of the object from Postgres
        self.id = id

        #  The client id (like the user id)
        self.clientId = client_id

        # set the expiry attribute to 30 minutes
        self.exp = datetime.utcnow() + timedelta(seconds=expires_seconds)
