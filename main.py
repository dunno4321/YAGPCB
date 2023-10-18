from flask import Flask, request
from threading import Thread
from bot import Bot
import logging
import random
import json
import time

app = Flask(__name__)
has_token = False
token = None
with open("assets/log.log", "w") as file:
    file.write("")
logging.basicConfig(filename="assets/log.log", level=logging.DEBUG)
logging.info("Hello world!")


def parse(url_):
    logging.debug("Parsing URL: " + url_)
    try:
        url_ = url_[url_.rfind("?") + 1:]
        params2 = url_.split("&")
        params = {}
        for item in params2:
            tmp = item.split("=")
            params[tmp[0]] = tmp[1]
        logging.info(f"Parsed URL to: {params}")
        return params
    except Exception as e:
        logging.error("Error parsing URL: " + str(e))
        return {}


@app.route("/token")
def home():
    global token, has_token
    logging.debug("Request on " + request.url)
    params = parse(request.url)
    if "code" in list(params.keys()):
        has_token = True
        token = params["code"]
        with open("assets/token.json", "w") as file:
            json.dump({"token": token}, file)
        logging.info("Successfully got token!")
        return "Successfully authorized!"
    else:
        has_token = False
        token = f"error: {params['error']}: {params['error_description']}"
        logging.error(f"Error getting token: {token}")
        print("Error getting token:")
        print(token)
        return token


def token_callback():
    return token


app_thread = Thread(target=app.run, kwargs={"port": 3000, "host": "0.0.0.0"})
bot = None
try:
    logging.info("Starting Flask thread...")
    app_thread.start()
    # allow time for the Flask info to get put to console before the link
    time.sleep(0.2)
    bot = Bot("assets/client_config.json", token_callback)
    bot.run()
except KeyboardInterrupt:
    if bot is not None:
        bot.close()
    app_thread.join(timeout=0)
