from flask import Flask, request, render_template, jsonify
from threading import Thread
from flask_cors import CORS
import logging
import json
import copy

app = Flask(__name__)
CORS(app)
app_thread = None


class ConfigData:
    has_code = False
    code = None

    data_from_botpy = None
    botpy_config_data = {"client_id": "", "client_secret": "", "channel": ""}

    new_update_req = False
    update_req_data = {"ads": False}

    new_repeating_task = False
    new_task_data = None

    remove_repeating_task = False
    remove_task_name = None

    tasks = []


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


def clean(text):
    allowed = "qwertuiopasdfghjklzxcvbnmQWETYUIOPASDFGHJKLZXCVBNM"
    builder = ""
    for char in list(text):
        if char in allowed:
            builder += char
    return builder


@app.route("/log")
def log_file():
    with open("assets/log.log") as file:
        return file.read().replace("\n", "<br><br>")


@app.route("/remove_repeating", methods=["POST"])
def remove_repeating():
    ConfigData.remove_repeating_task = True
    ConfigData.remove_task_name = request.json["name"]
    # def bruh(task):
    #     return clean(task["data"]["title"]) if task["data"]["type"] == "poll" else clean(task["data"]["msg_body"])
    # ConfigData.tasks = [task for task in ConfigData.tasks if bruh(task).replace(" ", "_") == request.json["name"]]
    return jsonify({"success": True, "message": "success"})


@app.route("/get_repeating")
def get_repeating():
    tasks = copy.deepcopy(ConfigData.tasks)
    for task in tasks:
        if task["data"]["type"] == "msg":
            task["name"] = task["data"]["msg_body"]
        else:
            task["name"] = task["data"]["title"]
    return jsonify(tasks)


@app.route("/poll", methods=["POST"])
def add_poll():
    data = request.json
    try:
        freq = float(data["freq_val"])
        freq /= (1 if data["freq_units"] == "minutes" else 60)
        data["freq_val"] = freq
    except Exception as e:
        print("nuh uh:", e)
        return jsonify({"success": False, "msg": "invalid frequency value"})
    # ConfigData.tasks.append({
    #     "name": data["msg_body"],
    #     "frequency": freq,
    #     "type": "poll",
    #     "enabled": True,
    #     "data": data
    # })
    data["type"] = "poll"
    ConfigData.new_repeating_task = True
    ConfigData.new_task_data = data
    return jsonify({"success": True, "message": "success"})


@app.route("/msg", methods=["POST"])
def add_msg():
    data = request.json
    try:
        freq = float(data["freq_val"])
        freq /= (1 if data["freq_units"] == "minutes" else 60)
        data["freq_val"] = freq
    except Exception as e:
        print("nuh uh:", e)
        return jsonify({"success": False, "msg": "invalid frequency value"})
    data["type"] = "msg"
    ConfigData.new_repeating_task = True
    ConfigData.new_task_data = data
    return jsonify({"success": True, "message": "success"})


def start_server():
    app_thread = Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 3000})
    app_thread.start()


def end_server():
    global app_thread
    if app_thread is not None:
        app_thread.join(0)
