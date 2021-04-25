# Extension to detect Phishing

## Setup

### Chrome Extension
- Navigate to chrome://extensions
- Toggle the "Developer mode" button to on (if not already done)
- Click on the “Load Unpacked” button
- Navigate to the local folder containing the `${PROJECT_ROOT}/extension` path
- The extension should load into your browser

### Server

#### Running the server using Docker
- Install Docker
- From the project root, run `docker build --tag phish-server .`. This will build the image 'phish-server'
- Run the container - `docker run -p 9999:9999 phish-server`. This should setup a server running in port 9999.

#### Running the server in local environment (without docker)
- Go into the `{ROOT}/server` and run `. venv/bin/activate` to activate the virtual env 
- Run `pip install -r requirements.txt` to install dependencies.
- Set `export FLASK_ENV=development` for enabling debugging (auto-reload, descriptive error messages)
- Run `python app.py` to start the server
- Create an `.env` file with content as `PR_API=<open-page-rank-API-key>`. The API can be retrieved for free at [Open Page Rank](https://www.domcop.com/openpagerank/auth/signup).

#### Endpoints 
- `POST /detect` 
Here's a curl request -
```
curl --location --request POST 'localhost:9999/detect' \
--form 'url="http://stackoverflow.com"'
```
The only data this post request requires is a url field that sends the url of the page.
