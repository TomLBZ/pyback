from typing import Any
from connexion.lifecycle import ConnexionResponse
from api.types import FileDict
import requests

class Response(dict):
    def __init3__(self, success: bool, msg: str, data: dict):
        self["success"] = success
        self["msg"] = msg
        self["data"] = data
    def __init1__(self, json: dict):
        self.__init3__(json["success"], json["msg"], json["data"] if "data" in json else {})
    def __init__(self, *args):
        if len(args) == 1:
            self.__init1__(args[0])
        elif len(args) == 3:
            self.__init3__(*args)
        else:
            raise ValueError("Invalid number of arguments")
    def toJsonResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="application/json", body=self)
    def toOctetResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="application/octet-stream", body=bytes(self["data"]))
    
class Server:
    def __init__(self, address: str) -> None:
        self.address_base = address

    def _res_to_response(self, res: requests.Response) -> Response:
        if (res.status_code != 200):
            return Response(False, "Failed to connect to Server", {})
        try:
            return Response(res.json())
        except: # non-json, may be downloading a file
            return Response(True, "Downloaded file", res.content)

    def _post(self, addr: str, json: dict | Any) -> Response:
        json = json.to_json() if hasattr(json, "to_json") else json
        res = requests.post(self.address_base + addr, json=json)
        return self._res_to_response(res)
    
    def _post_multipart(self, addr: str, body: dict, fileParams: FileDict) -> Response:
        res = requests.post(self.address_base + addr, data=body, files=fileParams)
        return self._res_to_response(res)
    
    def _get(self, addr: str) -> Response:
        res = requests.get(self.address_base + addr)
        return self._res_to_response(res)

    def _put(self, addr: str, json: dict | Any) -> Response:
        json = json.to_json() if hasattr(json, "to_json") else json
        res = requests.put(self.address_base + addr, json=json)
        return self._res_to_response(res)
    
    def _delete(self, addr: str) -> Response:
        res = requests.delete(self.address_base + addr)
        return self._res_to_response(res)