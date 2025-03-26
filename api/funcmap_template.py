from bridge.mdb import Mdb
from api.auth import UserManager
from api.secret import Secret
from bridge.deploy_template import Deployment

sec = Secret()
mdb = Mdb(sec.mdb_url, sec.mdb_name)
mng = UserManager(mdb, timeout_seconds=sec.auth_timeout)
svr = Deployment(sec.aero_address)

def uniSave(data):
    cname, data = data['cname'], data['data']
    res = mdb.update_all(cname, data, remove_old=True, upsert=True)
    return {"success": res}

def uniGet(data):
    cname = data['cname']
    results = mdb.find_all(cname, remove_id=True)
    return {"results": results}

def echo(op, data):
    return {"op": op, "data": data}

def error(msg):
    return {"error": msg}

funcMap = {
    "echo": echo,
    "error": error,
    "login": mng.login,
    "testlogin": mng.testlogin,
    "get": uniGet,
    "save": uniSave,
    "br/health": svr.get_health,
    "files/upload": svr.post_upload_file,
}