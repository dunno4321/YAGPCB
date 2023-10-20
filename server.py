from flask import Flask, request, render_template
from threading import Thread
import logging
import json
import copy

app = Flask(__name__)
app_thread = None


class ConfigData:
    has_code = False
    code = None

    data_from_botpy = None
    botpy_config_data = {"client_id": "", "client_secret": "", "channel": ""}

    new_update_req = False
    update_req_data = {"ads": False}


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
def token():
    logging.debug("Request on " + request.url)
    params = parse(request.url)
    if "code" in list(params.keys()):
        ConfigData.has_code = True
        ConfigData.code = params["code"]
        with open("assets/token.json", "w") as file:
            json.dump(params, file)
        logging.info("Successfully got token!")
        return "Successfully authorized!"
    else:
        ConfigData.has_code = False
        token = f"error: {params['error']}: {params['error_description']}"
        logging.error(f"Error getting token: {token}")
        print("Error getting token:")
        print(token)
        return token


@app.route("/")
def home():
    logging.info("Request on /")
    if ConfigData.data_from_botpy is not None:
        default = copy.deepcopy(ConfigData.data_from_botpy["default_commands"])
        custom = copy.deepcopy(ConfigData.data_from_botpy["custom_commands"])
        for cmd in default:
            cmd["checkbox"] = f'''<input type="checkbox" id="{cmd['name']}" onclick="send_('{cmd['name']}')"{' checked' if cmd['enabled'] else ''}>'''
        for cmd in custom:
            cmd["checkbox"] = f'''<input type="checkbox" id="{cmd['name']}" onclick="send_('{cmd['name']}')"{' checked' if cmd['enabled'] else ''}>'''

        return render_template("index.html", default_commands=default, custom_commands=custom, **ConfigData.botpy_config_data)
    else:
        with open("assets/misc_data.json") as file:
            data = json.load(file)
        default = copy.deepcopy(data["default_commands"])
        custom = copy.deepcopy(data["custom_commands"])
        for cmd in default:
            cmd["checkbox"] = f'''<input type="checkbox" id="{cmd['name']}" onclick="send_('{cmd['name']}')"{' checked' if cmd['enabled'] else ''}>'''
        for cmd in custom:
            cmd["checkbox"] = f'''<input type="checkbox" id="{cmd['name']}" onclick="send_('{cmd['name']}')"{' checked' if cmd['enabled'] else ''}>'''
        return render_template("index.html", default_commands=default, custom_commands=custom, **ConfigData.botpy_config_data)


@app.route("/update_data", methods=["GET"])
def scuffed_updated_config():
    logging.info(f"Request on {request.url}")
    params = parse(request.url)
    key = list(params.keys())[0]
    if params[key] == "true":
        print(f"Enabling command: {key}")
        ConfigData.new_update_req = True
        ConfigData.update_req_data = {key: True}
    else:
        print(f"Disabling command: {key}")
        ConfigData.new_update_req = True
        ConfigData.update_req_data = {key: False}
    return "updated successfully"


@app.route("/set_client_config")
def update_client_config():
    logging.info("Request on " + request.url)
    params = parse(request.url)
    keys = list(params.keys())
    with open("assets/client_config.json") as file:
        data = json.load(file)
    # there are faster ways to do this but this way should avoid the ability to put extra data info client_config.json
    for tmpkey in ["client_id", "client_secret", "channel"]:
        if tmpkey in keys:
            data[tmpkey] = params[tmpkey]
    with open("assets/client_config.json", "w") as file:
        json.dump(data, file)
    logging.info("Client config updated")
    print("Client config updated, restart the bot to use updated config")
    return "yoinked"


@app.route("/log")
def log_file():
    with open("assets/log.log") as file:
        return file.read().replace("\n", "<br><br>")


def start_server():
    app_thread = Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 3000})
    app_thread.start()


def end_server():
    if app_thread is not None:
        app_thread.join(0)
