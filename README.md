# Extension to detect Phishing

## Local Setup
TODO:

### Server
- Go into the `{ROOT}/server` and run `. venv/bin/activate` to activate the virtual env 
- Run `pip install -r requirements.txt` to install dependencies.
- Set `export FLASK_ENV=development` for enabling debugging (auto-reload, descriptive error messages)
- Run `python app.py` to start the server


#### Endpoints 
- `POST /detect`
Here's a curl request -
```
curl --location --request POST 'localhost:9999/detect' \
--form 'url="http://stackoverflow.com"'
```
The only data this post request requires is a url field that sends the url of the page.


## NOTES:
- Going with building an extension with Chrome, since there's a lot of literature about it. Should ideally work with all Chromium based browsers. Need to test it out later.
- Following this - https://css-tricks.com/how-to-build-a-chrome-extension/
- There are a lot of boilerplates already available, but trying the basic thing out first. If it gets tougher, will use a boiler-plate (Our use-case is not convoluted).
- Ended up using https://extensionizr.com/. It's exactly what I wanted. No chip-chip no jhik-jhik.


