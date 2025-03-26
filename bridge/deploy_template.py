from connexion.lifecycle import ConnexionResponse
from bridge.server import Server

class Deployment(Server):
    # ======= General GETs =======
    def get_health(self) -> ConnexionResponse:
        return self._get("/health").toJsonResponse()
    
    # ======= General POSTs =======
    def post_upload_file(self, data: dict) -> ConnexionResponse:
        return self._post_multipart("/upload_file", data).toJsonResponse()