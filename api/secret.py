import os
import json
from urllib.parse import quote_plus

class Secret:
    def __init__(self):
        self.secret_json = os.path.join(os.path.dirname(__file__), "..", "secrets", "config.json")
        self.secret_obj = json.load(open(self.secret_json))
        # mdb
        _mdb = self.secret_obj["mdb"]
        _mdb_user = _mdb["user"]
        _mdb_password = _mdb["password"]
        _mdb_url = _mdb["url"]
        self.mdb_name = _mdb["dbname"]
        self.mdb_url = self.encode_mdbstr(_mdb_user, _mdb_password, _mdb_url)
        # auth
        _auth = self.secret_obj["auth"]
        self.auth_timeout = _auth["timeout"]
        # ai
        _ai = self.secret_obj["ai"]
        self.ai_key = _ai["key"]
        self.ai_endpoint = _ai["endpoint"]
        # server
        _svr = self.secret_obj["server"]
        self.svr_address = _svr["address"]

    def encode_mdbstr(self, user: str, password: str, url: str):
        user = quote_plus(user)
        password = quote_plus(password)
        return url.format(user=user, password=password)