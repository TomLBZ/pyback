from typing import Any
from connexion.lifecycle import ConnexionResponse
import requests, json

class Response(dict):
    def __init3__(self, success: bool, msg: str, data: dict):
        self["success"] = success
        self["msg"] = msg
        self["data"] = data
    def __init1__(self, data: dict):
        s = data.get("success", False)
        m = data.get("msg", "No Message")
        d = data.get("data", {})
        if d == {} and m == "No Message" and s == False:
            self.__init3__(False, "Invalid response format", data)
        else:
            self.__init3__(s, m, d)
    def __init__(self, *args):
        if len(args) == 1:
            self.__init1__(args[0])
        elif len(args) == 3:
            self.__init3__(*args)
        else:
            raise ValueError("Invalid number of arguments")
    def toJsonResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="application/json", body=self["data"])
    def toOctetResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="application/octet-stream", body=bytes(self["data"]))
    def toAutoResponse(self) -> ConnexionResponse:
        if isinstance(self["data"], bytes):
            return self.toOctetResponse()
        return self.toJsonResponse()
    
class Server:
    def __init__(self, address: str) -> None:
        self.address_base = address

    def _res_to_response(self, res: requests.Response) -> Response:
        prefix = "Success" if res.ok else "Failed"
        content_type = res.headers.get("Content-Type", "unknown")
        data = res.json() if content_type == "application/json" \
            else res.content if content_type == "application/octet-stream" \
            else res.text if content_type == "text/html" \
            else f"Unsupported content type: {content_type}"
        return Response(res.ok, f"{prefix} {res.status_code}:", data)

    def _to_dict(self, data: dict | bytes | Any) -> str:
        if isinstance(data, dict):
            return data
        elif (hasattr(data, "to_json")):
            return data.to_json()
        elif isinstance(data, bytes):
            return json.loads(data.decode("utf-8"))
        return {"data": data}

    def _post(self, addr: str, data: dict | Any) -> Response:
        data = self._to_dict(data)
        res = requests.post(self.address_base + addr, json=data)
        return self._res_to_response(res)
    
    def _post_multipart(self, addr: str, data: dict | Any) -> Response:
        data = self._to_dict(data)
        res = requests.post(self.address_base + addr, files=data)
        return self._res_to_response(res)
    
    def _get(self, addr: str) -> Response:
        res = requests.get(self.address_base + addr)
        return self._res_to_response(res)

    def _put(self, addr: str, data: dict | Any) -> Response:
        data = self._to_dict(data)
        res = requests.put(self.address_base + addr, json=data)
        return self._res_to_response(res)
    
    def _delete(self, addr: str) -> Response:
        res = requests.delete(self.address_base + addr)
        return self._res_to_response(res)