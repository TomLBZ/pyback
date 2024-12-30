from connexion import AsyncApp
from pathlib import Path
from starlette.middleware.cors import CORSMiddleware

app = AsyncApp(__name__, specification_dir='./')
app.add_api('api.yaml')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex='.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    app.run(f"{Path(__file__).stem}:app", host='0.0.0.0', port=8000)