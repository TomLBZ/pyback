from bridge.mdb import Mdb
from api.auth import UserManager
from api.secret import Secret

sec = Secret()
mdb = Mdb(sec.mdb_url, sec.mdb_name)
mng = UserManager(mdb, timeout_seconds=sec.auth_timeout)

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