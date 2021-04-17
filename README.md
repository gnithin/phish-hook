# Extension to detect Phishing

## Local Setup
TODO:

### Server
- Go into the `{ROOT}/server` and run `. venv/bin/activate` to activate the virtual env 
- Run `pip install -r requirements.txt` to install dependencies.
- Set `export FLASK_ENV=development` for enabling debugging (auto-reload, descriptive error messages)
- Run `python app.py` to start the server

## NOTES:
- Going with building an extension with Chrome, since there's a lot of literature about it. Should ideally work with all Chromium based browsers. Need to test it out later.
- Following this - https://css-tricks.com/how-to-build-a-chrome-extension/
- There are a lot of boilerplates already available, but trying the basic thing out first. If it gets tougher, will use a boiler-plate (Our use-case is not convoluted).
- Ended up using https://extensionizr.com/. It's exactly what I wanted. No chip-chip no jhik-jhik.


