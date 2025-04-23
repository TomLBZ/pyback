from typing import Any
from connexion.lifecycle import ConnexionResponse
import requests, json

class Response(dict):
    def __init4__(self, success: bool, msg: str, data: dict, ctype: str):
        self["success"] = success
        self["msg"] = msg
        self["data"] = data
        self["content_type"] = ctype
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
        elif len(args) == 4:
            self.__init4__(*args)
        else:
            raise ValueError("Invalid number of arguments")
    def toJsonResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="application/json", body=self["data"])
    def toFileResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="application/octet-stream", body=bytes(self["data"]))
    def toTextResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="text/plain", body=str(self["data"]))
    def toHtmlResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="text/html", body=str(self["data"]))
    def toCsvResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="text/csv", body=str(self["data"]))
    def toXmlResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="application/xml", body=str(self["data"]))
    def toYamlResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="application/x-yaml", body=str(self["data"]))
    def toFormResponse(self) -> ConnexionResponse:
        return ConnexionResponse(status_code=200, content_type="application/x-www-form-urlencoded", body=str(self["data"]))
    def toAutoResponse(self) -> ConnexionResponse:
        if isinstance(self["data"], bytes):
            return self.toFileResponse()
        elif isinstance(self["data"], dict):
            return self.toJsonResponse()
        elif isinstance(self["data"], str):
            ctype = self.get("content_type", "unknown")
            if "application/json" in ctype:
                return self.toJsonResponse()
            elif "application/octet-stream" in ctype:
                return self.toFileResponse()
            elif "application/x-www-form-urlencoded" in ctype:
                return self.toFormResponse()
            elif "application/xml" in ctype:
                return self.toXmlResponse()
            elif "application/x-yaml" in ctype:
                return self.toYamlResponse()
            elif "text/csv" in ctype:
                return self.toCsvResponse()
            elif "text/html" in ctype:
                return self.toHtmlResponse()
            elif "text/plain" in ctype:
                return self.toTextResponse()
            else:
                return self.toTextResponse()
        else:
            return self.toTextResponse()
    
class Server:
    def __init__(self, address: str) -> None:
        self.address_base = address

    def _res_to_json(self, res: requests.Response) -> dict:
        try:
            return res.json()
        except json.JSONDecodeError:
            return {"success": False, "msg": "Invalid JSON response", "data": res.text}

    def _res_to_response(self, res: requests.Response) -> Response:
        prefix = "Success" if res.ok else "Failed"
        content_type = res.headers.get("Content-Type", "unknown")
        data = self._res_to_json(res) if "application/json" in content_type \
            else res.content if "application/octet-stream" in content_type \
            else res.text if "application/x-www-form-urlencoded" in content_type \
            else res.text if "application/xml" in content_type \
            else res.text if "application/x-yaml" in content_type \
            else res.text if "text/csv" in content_type \
            else res.text if "text/html" in content_type \
            else res.text if "text/plain" in content_type \
            else f"Unsupported content type: {content_type}"
        return Response(res.ok, f"{prefix} {res.status_code}:", data, content_type)

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