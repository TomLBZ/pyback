from bridge.mdb import Mdb
from datetime import datetime
from time import mktime

class UserManager:
    def __init__(self, mdb: Mdb, timeout_seconds=1800):
        self.mdb = mdb
        self.timeout_seconds = timeout_seconds
        self.letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def check_timeout(self):
        users = self.mdb.find("users", {"salt": {"$exists": True, "$ne": ""}}, remove_id=False)
        for user in users:
            datetimeobj: datetime = user["timestamp"]
            timenow = datetime.now()
            timediffsec = (timenow - datetimeobj).total_seconds()
            if timediffsec > self.timeout_seconds:
                self.mdb.update("users", {"name": user["name"]}, {"$set": {"salt": "", "timestamp": None}})

    def login(self, data):
        self.check_timeout()
        name, password = data['name'], data['password']
        user = self.mdb.find_one("users", {"name": name, "password": password}, remove_id=False)
        if user is None:
            return {"success": False, "user": name}
        oid = user.pop("_id")
        timenow = datetime.now()
        timestamp = timenow.strftime("%Y-%m-%d %H:%M:%S")
        timenum = mktime(timenow.timetuple())
        timenumsum = sum([int(c) for c in str(int(timenum))])
        random = "".join([self.letters[ord(c) % timenumsum] for c in f"{timestamp}{name}{password}"])
        random = "".join([self.letters[(self.letters.index(c) + timenumsum) % len(self.letters)] for c in random])
        roles = user["roles"]
        self.mdb.update("users", {"_id": oid}, {"$set": {"salt": random, "timestamp": timenow}})
        return {"success": True, "user": name, "timestamp": timestamp, "salt": random, "roles": roles}

    def testlogin(self, data):
        self.check_timeout()
        salt = data['salt']
        user = self.mdb.find_one("users", {"salt": salt}, remove_id=False)
        if user is None:
            return {"success": False, "user": None}
        return {"success": True, "user": user["name"]}