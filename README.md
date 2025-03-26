# pyback
Simple Python Backend API boilerplate, with:
1. For API entrances, the header contains an optional `token` field, which is used for authentication.
2. A unified API entrance on `/uniPostJson`, that listens for incoming POST requests containing a JSON body with the following structure:
    | Field | Type | Description | Required |
    | --- | --- | --- | --- |
    | op | string | The operation to be performed | Yes |
    | data | object | The data to be processed | Yes |
3. A unified API entrance on `/uniPostMultipart`, that listens for incoming POST requests containing Multipart / Form Data body with the following structure:
    | Field | Type | Description | Required |
    | --- | --- | --- | --- |
    | op | string | The operation to be performed | Yes |
    | data | object | The data to be processed | Yes |
    | file | string (binary) | The file to be processed | No |
    | files | array (of binary strings) | The files to be processed | No |
4. A simple example of a `GET` request on `/`, that returns a simple JSON response:
    ```json
    { "data": "Hello, World!" }
    ```

# Features
1. Auto-reload on code changes.
2. Supports relaying requests to other APIs.

# Usage
1. Clone this repo and cd into it
    ```bash
    git clone https://github.com/TomLBZ/pyback.git && cd pyback
    ```
2. Create and edit the secrets/config.json file
    ```bash
    cp secrets/config_template.json secrets/config.json
    vim secrets/config.json
    ```
3. Create and edit your own implementations of the `api/funcmap.py` and `bridge/deploy.py` files
    ```bash
    cp api/funcmap_template.py api/funcmap.py
    cp bridge/deploy_template.py bridge/deploy.py
    vim api/funcmap.py
    vim bridge/deploy.py
    ```
3. Toggle between development and production mode by changing the `command` field in the `compose.yaml` file
    ```bash
    vim compose.yaml
    ```
4. Start the container
    ```bash
    docker build -t pyback .
    docker compose up -d
    ```
    Development Mode Only:
    ```bash
    # Access the container
    docker exec -it pyback bash
    # Inside the container, start the server
    python3 app.py
    ```
5. Test the API
    ```bash
    curl http://localhost:18000
    ```