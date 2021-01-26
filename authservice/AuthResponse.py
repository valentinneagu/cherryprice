class AuthResponse(dict):

    def __init__(self, token, expires_in):
        super().__init__()
        self.token = token
        self.expires_in = expires_in
