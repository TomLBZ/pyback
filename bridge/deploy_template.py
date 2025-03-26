from connexion.lifecycle import ConnexionResponse
from api.types import FileDict
from bridge.server import Server

class Deployment(Server):
    # ======= General GETs =======
    def get_health(self) -> ConnexionResponse:
        return self._get("/health").toJsonResponse()
    
    # ======= General POSTs =======
    def post_upload_file(self, data: dict, fileParams: FileDict) -> ConnexionResponse:
        body = {'type': data}
        return self._post_multipart("/upload_file", body, fileParams).toJsonResponse()