# pyback
Simple Python Backend API boilerplate, with:
1. A unified API entrance on `/uniPost`, that listens for incoming POST requests containing a JSON body with the following structure:
    ```json
    {
        "op": "string",
        "data": "object | array | string | number | boolean"
    }
    ```
    The `op` field is used to determine the operation to be performed, and the `data` field is used to pass the data to be processed.
2. A simple example of a `GET` request on `/`, that returns a simple JSON response:
    ```json
    {
        "message": "Hello, World!"
    }
    ```
# Features
Auto-reload on code changes.

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
    # Exit the container
    exit
    ```
5. Test the API
    ```bash
    curl http://localhost:18000
    ```