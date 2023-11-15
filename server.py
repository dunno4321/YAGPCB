from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
from threading import Thread
from flask_cors import CORS
import logging
import random
import copy
import json


# set up logging and Flask
app = Flask(__name__)
CORS(app)
logger = logging.getLogger("server")
date_time_fmt = "%d/%m/%Y %H:%M:%S"


def dump_data(data):
    with open("./assets/data.json", "w") as file:
        json.dump(data, file)


def dump_giveaway(data):
    with open("./assets/giveaway.json", "w") as file:
        json.dump(data, file)


# parse urls into nice, easy-to-use dictionaries
def parse(url_):
    global logger
    logger.debug("Parsing URL: " + url_)
    try:
        url_ = url_[url_.rfind("?") + 1:]
        params2 = url_.split("&")
        params = {}
        for item in params2:
            tmp = item.split("=")
            params[tmp[0]] = tmp[1]
        logger.info(f"Parsed URL to: {params}")
        return params
    except Exception as e:
        logger.error("Error parsing URL: " + str(e))
        return {}


# cleans text to only allowed chars
def clean(text):
    allowed = "qwertuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    builder = ""
    for char in list(text):
        if char in allowed:
            builder += char
    return builder


# most of the @app.route functions are self-explanatory
# pretty simple logic
@app.route("/")
def home():
    logger.info("Request on /")
    instance = get_server_instance()
    default = copy.deepcopy(instance.data["default_commands"])
    custom = copy.deepcopy(instance.data["custom_commands"])

    # silly logic for enabling/disabling commands
    for cmd in default:
        cmd["checkbox"] = f'''<input type="checkbox" id="{cmd['name']}" onclick="send_('{cmd['name']}', true)"{' checked' if cmd['enabled'] else ''}>'''
    for cmd in custom:
        cmd["checkbox"] = f'''<input type="checkbox" id="{cmd['name']}" onclick="send_('{cmd['name']}', false)"{' checked' if cmd['enabled'] else ''}>'''

    return render_template("index.html", default_commands=default, custom_commands=custom,
                           **instance.config)


@app.route("/set_client_config")
def update_client_config():
    logger.info("Request on /set_client_config")
    params = parse(request.url)
    get_server_instance().set_config(params)
    logger.info("Client config updated")
    print("Client config updated, restart the bot to use updated config")
    return jsonify({"success": True, "msg": "config updated"})


@app.route("/token")
def token():
    logger.debug("Request on /token")
    inst = get_server_instance()
    params = parse(request.url)
    if "code" in list(params.keys()):
        inst.code = params["code"]
        with open("./assets/token.json", "w") as file:
            json.dump(params, file)
        logger.info("Successfully got code!")
        return jsonify({"success": True, "msg": "code yoinked"})
    else:
        logger.error(f"Error getting token: {params['error_description']}")
        logger.error("Error getting token:")
        logger.error(params['error_description'])
        return jsonify({"success": False, "msg": "failed to get token: " + params['error_description']})


@app.route("/log")
def log_file():
    logger.info("Request on /log")
    with open("./assets/log.log") as file:
        return file.read().replace("\n", "<br><br>")


# might want to add backend validation
# but this is a small app and won't be used by a lot of ppl, if anyone
# if for some this reason gets popular i'll add it
@app.route("/remove_repeating", methods=["POST"])
def remove_repeating():
    logger.info("Request on /remove_repeating")
    inst = get_server_instance()
    inst.remove_repeating_task(request.json["name"])
    return jsonify({"success": True, "message": "success"})


@app.route("/get_repeating")
def get_repeating():
    logger.info("Request on /get_repeating")
    tasks = copy.deepcopy(get_server_instance().data["repeating_tasks"])
    for task in tasks:
        if task["type"] == "msg":
            task["name"] = task["msg_body"]
        else:
            task["name"] = task["title"]
    return jsonify(tasks)


@app.route("/update_data")
def update_enabled():
    logger.info("Request on /update_data")
    inst = get_server_instance()
    params = parse(request.url)
    key = [key for key in list(params.keys()) if key != "is_default"][0]
    # js fetch passes the true/false as "true" or "false" strings in the url
    # eval("true".title()) == True
    # eval("false".title()) == False
    params[key] = eval(params[key].title())
    if params[key]:
        inst.enable_command(key, params["is_default"])
    else:
        inst.disable_command(key, params["is_default"])
    return jsonify({"yoinked": True})


@app.route("/poll", methods=["POST"])
def add_poll():
    logger.info("Request on /poll")
    inst = get_server_instance()
    data = request.json
    try:
        freq = float(data["freq_val"])
        freq /= (1 if data["freq_units"] == "minutes" else 60)
        data["freq_val"] = freq
    except Exception as e:
        logger.error("err in add_poll: " + str(e))
        return jsonify({"success": False, "msg": "invalid frequency value"})
    data["type"] = "poll"
    data["next"] = (datetime.now() + timedelta(minutes=data["freq_val"])).strftime(date_time_fmt)
    inst.add_repeating_task(data)
    return jsonify({"success": True, "message": "success"})


@app.route("/msg", methods=["POST"])
def add_msg():
    inst = get_server_instance()
    data = request.json
    try:
        freq = float(data["freq_val"])
        freq /= (1 if data["freq_units"] == "minutes" else 60)
        data["freq_val"] = freq
    except Exception as e:
        logger.error("err in add_msg: " + str(e))
        return jsonify({"success": False, "msg": "invalid frequency value"})
    data["type"] = "msg"
    data["next"] = (datetime.now() + timedelta(minutes=data["freq_val"])).strftime(date_time_fmt)
    inst.add_repeating_task(data)
    return jsonify({"success": True, "message": "success"})


@app.route("/get_giveaway")
def get_giveaway():
    inst = get_server_instance()
    inst.refresh_giveaway_data()
    data = copy.deepcopy(inst.get_giveaway_data())
    if data != {}:
        data["entrants"] = len(list(data["entrants"].keys()))
    return jsonify(data if data != {} else {"active": False})


@app.route("/add_giveaway", methods=["POST"])
def add_giveaway():
    inst = get_server_instance()
    inst.set_giveaway_data(request.json)
    return jsonify({"success": True, "msg": "added giveaway"})


@app.route("/cancel_giveaway")
def cancel_giveaway():
    inst = get_server_instance()
    inst.cancel_giveaway()
    return jsonify({"success": True, "msg": "Successfully cancelled the giveaway"})


@app.route("/end_giveaway")
def end_giveaway():
    inst = get_server_instance()
    winner, msg = inst.end_giveaway()
    if winner:
        return jsonify({"success": True, "msg": "Successfully ended the giveaway", "winner": winner})
    else:
        return jsonify({"success": False, "msg": msg})


# no global vars
# such wow, vary fancy
def get_server_instance():
    if Server.instance is None:
        Server.instance = Server()
    return Server.instance


class Server:
    # such fancy
    instance = None

    def __init__(self):
        if Server.instance is not None:
            raise Exception("Only one Server class allowed!")
        else:
            logger.info("Creating Server instance...")
            Server.instance = self
        self.app = app

        with open("./assets/data.json") as file:
            self.data = json.load(file)
        now = datetime.now()
        for task in self.data["repeating_tasks"]:
            task["next"] = (now + timedelta(minutes=task["freq_val"])).strftime(date_time_fmt)
        self.code = None
        self.token = None
        with open("./assets/config.json") as file:
            self.config = json.load(file)

        self.thread = Thread(target=self.app.run, kwargs={"host": "0.0.0.0", "port": 3000})
        self.thread.start()

        with open("./assets/giveaway.json") as file:
            self.giveaway_data = json.load(file)
        self.cancel_giveaway_ = None
        self.end_giveaway_ = None

    # most of these are self explanatory
    def set_config(self, config):
        self.config = config

    def set_data(self, data):
        self.data = data

    def get_config(self):
        return self.config

    def get_data(self):
        return self.data

    def add_repeating_task(self, data):
        self.data["repeating_tasks"].append(data)
        dump_data(self.data)

    def remove_repeating_task(self, data):
        def name_(item):
            return clean(item["msg_body"] if item["type"] == "msg" else item["title"]).lower()
        name = clean(data).lower()
        self.data["repeating_tasks"] = [task for task in self.data["repeating_tasks"] if name_(task) != name]
        dump_data(self.data)

    def add_command(self, name, returns, enabled):
        self.data["custom_commands"].append({
            "name": name,
            "return": returns,
            "enabled": enabled
        })
        dump_data(self.data)

    def remove_command(self, name):
        self.data["custom_commands"] = [cmd for cmd in self.data["custom_commands"] if cmd["name"].lower() != name]
        dump_data(self.data)

    def enable_command(self, name, is_default):
        logger.info("enabling " + name)
        commands_ = self.data["default_commands"] if is_default else self.data["custom_commands"]
        commands_ = [item for item in commands_ if item["name"].lower() == name.lower()]
        for match in commands_:
            # doesn't need to set it back because lists/dicts are passed by ref
            match["enabled"] = True
        dump_data(self.data)

    def disable_command(self, name, is_default):
        logger.info("disabling " + name)
        commands_ = self.data["default_commands"] if is_default else self.data["custom_commands"]
        commands_ = [item for item in commands_ if item["name"].lower() == name.lower()]
        for match in commands_:
            # doesn't need to set it back because lists/dicts are passed by ref
            match["enabled"] = False
        dump_data(self.data)

    def is_command_enabled(self, name, is_default):
        commands_ = self.data["default_commands"] if is_default else self.data["custom_commands"]
        commands_ = [item for item in commands_ if item["name"].lower() == name.lower()]
        if len(commands_) == 0:
            return False
        return commands_[0]["enabled"]

    def refresh_giveaway_data(self):
        with open("./assets/giveaway.json") as file:
            self.giveaway_data = json.load(file)

    def get_giveaway_data(self):
        return self.giveaway_data

    def set_giveaway_data(self, data):
        try:
            data["ticket_cost"] = int(data["ticket_cost"])
        except ValueError:
            data["ticket_cost"] = 50
        data["active"] = True
        data["entrants"] = {}
        self.giveaway_data = data
        dump_giveaway(data)

    def cancel_giveaway(self):
        self.cancel_giveaway_ = True
        if self.giveaway_data is not None:
            self.giveaway_data["active"] = False
            logger.info(f"Cancelled active giveaway: {self.giveaway_data['title']}")
            dump_giveaway(self.giveaway_data)

    def end_giveaway(self):
        self.end_giveaway_ = True
        if self.giveaway_data is not None:
            self.giveaway_data["active"] = False
            winner = random.choice(list(self.giveaway_data["entrants"].keys()))
            self.giveaway_data["winner"] = winner
            logger.info(f"Giveaway {self.giveaway_data['title']} ended with a winner of {winner}")
            dump_giveaway(self.giveaway_data)
            return winner, ""
        return False, "No active giveaway"
