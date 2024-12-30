from bridge.mdb import Mdb
from api.auth import UserManager
import os
import json

# config.json is locates at project_root/secrets/config.json
secret_json = os.path.join(os.path.dirname(__file__), "..", "secrets", "config.json")
secret_obj = json.load(open(secret_json))

mdb = Mdb(secret_obj["mdbstr"], "devdb")
mng = UserManager(mdb, timeout_seconds=1800)

def login(data):
    return mng.login(data)

def testlogin(data):
    return mng.testlogin(data)

def uniget(data):
    cname = data['cname']
    results = mdb.find_all(cname, remove_id=True)
    return {"results": results}

def unisave(data):
    cname, data = data['cname'], data['data']
    res = mdb.update_all(cname, data, remove_old=True, upsert=True)
    return {"success": res}

funcMap = {
    "login": login,
    "testlogin": testlogin,
    "get": uniget,
    "save": unisave,
}

def uniPost(body):
    op, data = body['op'], body['data']
    if op in funcMap:
        return funcMap[op](data)
    return f"Operation: {op}, Data: {data}"

def uniPostOptions():
    return {"message": "Options"}