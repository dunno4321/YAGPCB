from server import ConfigData, start_server, clean
from datetime import datetime, timedelta
from twitchio.ext import commands
from twitchio import Message
from threading import Thread
import requests
import asyncio
import logging
import random
import json
import time


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


def random_quote(ctx: commands.Context):
    logging.info(f"Getting random quote for streamer {ctx.channel.name}")
    streamer = ctx.channel.name
    with open("assets/quotes.json") as file:
        tmp = json.load(file)
    tmp = [quote for quote in tmp if quote["streamer"] == streamer]
    if len(tmp) == 0:
        logging.warning("No quotes found!")
    return format_quote(random.choice(tmp)) if len(tmp) > 0 else "No quotes found for this streamer!"


def format_quote(quote):
    return f"{quote['streamer']} said '{quote['msg']}' on {quote['added']} (#{quote['num']}), as quoted by {quote['quoter']}"


def add_quote(ctx: commands.Context):
    logging.info(f"Adding quote for streamer {ctx.channel.name}")
    with open("assets/quotes.json") as file:
        tmp = json.load(file)
        tmp = [item for item in tmp if item["streamer"] == ctx.channel.name]

    msg = ctx.message.content
    data = {
        "quoter": ctx.message.author.name,
        "msg": msg[msg.find(" ") + 1:].replace('"', "").strip(),
        "num": len(tmp) + 1,
        "added": datetime.now().strftime("%m/%d/%Y"),
        "streamer": ctx.channel.name
    }

    tmp.append(data)

    with open("assets/quotes.json", "w") as file:
        json.dump(tmp, file, indent=2)
    return len(tmp)


class Bot(commands.Bot):
    def __init__(self, config_file, channels=None):
        start_server()
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            with open(config_file) as file:
                config = json.load(file)
        except FileNotFoundError:
            logging.error(f"{config_file} not found!")
            raise Exception(f"{config_file} not found, please run set_stuff.py with the command 'python set_stuff.py'")
        tmp = list(config.keys())
        tmp.sort()
        self._wait_for_flask = False
        if tmp != ['channel', 'client_id', 'client_secret']:
            with open(config_file, "w") as file:
                json.dump({"client_id": "", "client_secret": "", "channel": ""}, file, indent=2)
            self._wait_for_flask = True
        if config["channel"] == "" or config["client_id"] == "" or config["client_secret"] == "":
            logging.error("Default config detected, will wait for Flask input...")
            self._wait_for_flask = True

        self._has_token = False

        if self._wait_for_flask:
            print(f"Waiting for web input @ http://localhost:3000")
            while not ConfigData.has_code:
                pass

        if channels is None:
            channels = [config['channel']]

        self._config = config
        ConfigData.botpy_config_data = config

        self.has_token = False
        self._token = self.get_access_token(lambda x: ConfigData.code)
        print("Attempting connection...")
        logging.info("Attempting connection...")
        # sometimes a new token needs a second to actually work :3
        time.sleep(5)
        super().__init__(token=self._token, prefix="!", initial_channels=channels,
                         client_secret=config["client_secret"])
        self._channel = None
        self._connected = False
        self._user = self._get_user(config["channel"])
        self._active = True
        self._chatters_checked_at = datetime.now() - timedelta(hours=1)
        self._moderators = self._get_moderators()
        self._vips = self._get_vips()
        self._cheated_n_times = 0
        self._thread = Thread(target=self._worker_thread)
        self._thread.start()
        with open("assets/misc_data.json") as file:
            self._misc_data = json.load(file)
        now = datetime.now()
        for task in self._misc_data["repeating_tasks"]:
            task["next_occurrence"] = (now + timedelta(minutes=task["data"]["freq_val"])).strftime("%d/%m/%Y %H:%M:%S")
        self._default_cmds_list = [item["name"] for item in self._misc_data["default_commands"]]
        print("Connected! Config page: http://localhost:3000")

    def _is_command_enabled(self, command: str, is_default: bool = True):
        # shush
        for cmd in self._misc_data["default_commands" if is_default else "custom_commands"]:
            if command.lower() == cmd["name"]:
                return cmd["enabled"]
        return False

    async def event_message(self, message: Message):
        msg = message.content.strip()
        # avoid weird threading things
        if msg.startswith("!"):
            cmd = msg.split()[0].replace("!", "")
            tmp2 = [tmp for tmp in self._misc_data["custom_commands"] if tmp["name"] == cmd]
            if len(tmp2) != 0:
                tmp2 = tmp2[0]
                logging.info(f"Custom command {cmd} called by {message.author.name}")
                if tmp2["enabled"]:
                    await message.channel.send(tmp2["return"])
                else:
                    await message.channel.send("Command disabled by streamer")
            else:
                await self.handle_commands(message)

    def _get_vips(self):
        res = self._get(f"https://api.twitch.tv/helix/channels/vips?broadcaster_id={self._user.id}")
        try:
            return [vip["user_login"] for vip in res["data"]]
        except KeyError:
            print(res)

    def _get_moderators(self):
        res = self._get(f"https://api.twitch.tv/helix/moderation/moderators?broadcaster_id={self._user.id}")
        try:
            return [mod["user_login"] for mod in res["data"]]
        except KeyError:
            print(res)

    def refresh_token(self):
        logging.info("Refreshing access token...")
        response = requests.post("https://id.twitch.tv/oauth2/token",
                                 headers={"Content-Type": "application/x-www-form-urlencoded"},
                                 data=f"grant_type=refresh_token&refresh_token={self._token_data['refresh_token']}&client_id={self._config['client_id']}&client_secret={self._config['client_secret']}")
        if response.status_code >= 400:
            print(f"Failed to refresh token (HTTP code {response.status_code}, https://http.cat/{response.status_code}")
            logging.error(
                f"Failed to refresh token (HTTP code {response.status_code}, https://http.cat/{response.status_code}")
        else:
            data = response.json()
            self._token_data["access_token"] = data["access_token"]
            self._token_data["refresh_token"] = data["refresh_token"]
            self._token_data["expires_in"] = (datetime.now() + timedelta(hours=3.5)).strftime("%d/%m/%Y %H:%M:%S")
            with open("assets/token.json", "w") as file:
                json.dump(self._token_data, file, indent=2)
            self._token = data["access_token"]
            logging.info("Successfully refreshed token!")

    def get_access_token(self, callback):
        try:
            logging.info("Attempting to get a previous token...")
            with open("assets/token.json") as file:
                data = json.load(file)
                self._token_data = data
        except FileNotFoundError:
            # get a new token, mildly sketchy logic
            logging.info("token.json not found, creating...")
            data = {"access_token": ""}
        # if the code will expire in less than an hour, get a new one
        if data["access_token"] == "" or "refresh_token" not in list(data.keys()):
            print("Connect to twitch via this link:")
            scopes = [
                "moderator:read:chatters",
                "chat:edit",
                "chat:read",
                "moderator:manage:shoutouts",
                "channel:manage:polls",
                "moderator:manage:chat_messages",
                "channel:manage:broadcast",
                "moderation:read",
                "channel:read:vips"
            ]
            logging.info(f"Scopes: {', '.join(scopes)}")
            # print("""https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=28jexim9tw3g8u52evmlqbpob96ymn&redirect_uri=http://localhost:3000&scope=moderator%3Aread%3Achatters%2Bchat%3Aedit%2Bchat%3Aread&state=c3ab8aa609ea11e793ae92361f002671""")
            print(f"""https://id.twitch.tv/oauth2/authorize
            ?response_type=code
            &client_id={self._config['client_id']}
            &redirect_uri=http://localhost:3000/token
            &scope={'+'.join(scopes)}""".replace("\n", "").replace(" ", "").strip())
            print("Waiting...")
            logging.info("Waiting for user...")
            while callback(0) is None:
                pass
            token = callback(0)
            response = requests.post("https://id.twitch.tv/oauth2/token",
                                     data=f"client_id={self._config['client_id']}&client_secret={self._config['client_secret']}&code={token}&grant_type=authorization_code&redirect_uri=http://localhost:3000/token").json()
            try:
                response["expires_in"] = (datetime.now() + timedelta(seconds=response["expires_in"] - 60))
                self._token_data = response
                response["expires_in"] = response["expires_in"].strftime("%d/%m/%Y %H:%M:%S")
                with open("assets/token.json", "w") as file:
                    json.dump(response, file, indent=2)

                logging.info(f"New token acquired: {token}")
                return token
            except Exception as e:
                logging.error(f"Error getting token: {str(e)}")
                logging.error("Most likely invalid client id/secret")
                raise Exception(
                    f"Error getting token: {str(e)}. Check your client_id and client_secret in client_config.json!")
        elif "refresh_token" in list(data.keys()) and data["refresh_token"] != "":
            self.refresh_token()
            return self._token
        elif datetime.strptime(data["expires_in"], "%d/%m/%Y %H:%M:%S") > (datetime.now() + timedelta(hours=1)):
            return data["access_token"]

    def _worker_thread(self):
        while self._active:
            now = datetime.now()

            if abs((now - datetime.strptime(self._token_data["expires_in"], "%d/%m/%Y %H:%M:%S")).total_seconds()) < 120:
                self.refresh_token()

            ConfigData.data_from_botpy = self._misc_data
            if ConfigData.new_update_req:
                cmd_name = list(ConfigData.update_req_data.keys())[0]
                enabled = ConfigData.update_req_data[cmd_name]
                if enabled:
                    self.enable_command(cmd_name)
                else:
                    self.disable_command(cmd_name)
                ConfigData.new_update_req = False
                ConfigData.botpy_config_data = self._config

            if ConfigData.new_repeating_task:
                data = ConfigData.new_task_data
                logging.info(f"New repeating task: {data}")
                ConfigData.new_repeating_task = False
                # TODO: input validation :3
                self._misc_data["repeating_tasks"].append({
                    "type": data["type"],
                    "frequency": int(data["freq_val"]),
                    "data": data,
                    "next_occurrence": (now + timedelta(minutes=data["freq_val"])).strftime("%d/%m/%Y %H:%M:%S")
                })
                logging.info(self._misc_data["repeating_tasks"])
                with open("assets/misc_data.json", "w") as file:
                    json.dump(self._misc_data, file, indent=2)

            if ConfigData.remove_repeating_task:
                tmp = self._misc_data["repeating_tasks"]
                tmp2 = []
                name = clean(ConfigData.remove_task_name)
                for item in tmp:
                    item_name = item["data"]["msg_body"] if item["type"] == "msg" else item["data"]["title"]
                    if clean(item_name) != name:
                        tmp2.append(item)
                # tmp = [item for item in tmp if clean(item["data"]["msg_body"] if item["type"] == "msg" else item["data"]["title"] != clean(ConfigData.remove_task_name))]
                self._misc_data["repeating_tasks"] = tmp2
                with open("assets/misc_data.json", "w") as file:
                    json.dump(self._misc_data, file, indent=2)
                ConfigData.remove_repeating_task = False

            for task in self._misc_data["repeating_tasks"]:
                time_ = datetime.strptime(task["next_occurrence"], "%d/%m/%Y %H:%M:%S")
                data = task["data"]
                if (now - time_).total_seconds() > 0:
                    logging.info("doing repeating task with data:", data)
                    if task["type"] == "poll":
                        """
                        title: title
                        options: options
                        c_points_enabled: true/false
                        c_points_per_vote: int
                        """
                        self.create_poll(data["title"], data["options"], channel_points=data["c_points_enabled"], points_per_vote=data["c_points_per_vote"], duration=data["duration"])
                    else:
                        """
                        msg_body: content
                        """
                        self._send_message(data["msg_body"])
                    task["next_occurrence"] = (now + timedelta(minutes=data["freq_val"])).strftime("%d/%m/%Y %H:%M:%S")
                    logging.info("next: " + task["next_occurrence"])

            ConfigData.tasks = self._misc_data["repeating_tasks"]

    def _send_message(self, content):
        if self._connected:
            if self._channel is None:
                self._channel = self.get_channel(self._config["channel"])
            self._loop.create_task(self._channel.send(content))
        else:
            logging.warning("Cannot send message because not connected yet :3")

    def _get(self, url):
        logging.debug(f"Getting url: {url}")
        return requests.get(url, headers={"Authorization": f"Bearer {self._token}",
                                          "Client-Id": self._config["client_id"]}).json()

    def _get_user(self, username):
        logging.info(f"Attempting to get user {username}")
        try:
            data = self._get(f"https://api.twitch.tv/helix/users?login={username}")["data"][0]
            logging.info(f"Successfully got user {data['display_name']} with ID {data['id']}")
            return self.create_user(data["id"], data["display_name"])
        except IndexError:
            # user does not exist
            logging.error(f"USer {username} does not exist!")
            return None
        except KeyError:
            logging.error("Token not valid ig, wait a few seconds")
            raise Exception("Twitch token being dumb, wait a few seconds then run again")

    async def event_ready(self):
        logging.info(f"Logged in as {self.nick} with ID {self.user_id}")
        logging.info(f"Connected to: {[channel.name for channel in self.connected_channels]}")
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as @{self.nick}')
        print(f'User id is {self.user_id}')
        print(f"Connected to these channels: {[channel.name for channel in self.connected_channels]}")
        self._connected = True

    @commands.command()
    async def hello(self, ctx: commands.Context):
        logging.info(f"!hello called by {ctx.author.name}")
        if not self._is_command_enabled("hello"):
            await ctx.send("Command disabled by streamer")
            return
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def ping(self, ctx: commands.Context):
        logging.info(f"!ping called by {ctx.author.name}")
        if not self._is_command_enabled("ping"):
            await ctx.send("Command disabled by streamer")
            return
        # pong
        await ctx.send(f'Pong!')

    @commands.command()
    async def addquote(self, ctx: commands.Context):
        logging.info(f"!addquote called by {ctx.author.name}")
        # if ctx.author.badges.get("vip") or ctx.author.badges.get("mod") or ctx.author.name == ctx.channel.name:
        user = ctx.message.author.name
        if user in self._moderators or user in self._vips or user == ctx.channel.name:
            if not self._is_command_enabled("addquote"):
                await ctx.send("Command disabled by streamer")
                return
            num_quotes = add_quote(ctx)
            logging.info(f"Added quote #{num_quotes}")
            await ctx.send(f"Successfully added quote #{num_quotes}")
        else:
            logging.info(f"{user} does not have permission to use this command!")
            await ctx.send("<3 you dont have permission to use this command <3")

    @commands.command()
    async def quote(self, ctx: commands.Context):
        logging.info(f"!quote called by {ctx.author.name}")
        if not self._is_command_enabled("quote"):
            await ctx.send("Command disabled by streamer")
            logging.info("Command disabled")
            return
        msg = ctx.message.content.strip().replace("\U000e0000", "")
        args = msg.split(" ")[1:]
        args = [item.strip() for item in args if len(item.strip()) > 0]
        if len(args) != 0:
            number = args[0]
            try:
                number = int(number)
                if number <= 0:
                    logging.error(f"{number} must be greater than 0!")
                    await ctx.send("Argument 'number' must be a number greater than 0!")
                else:
                    with open("assets/quotes.json") as file:
                        quotes = json.load(file)
                    quotes = [quote for quote in quotes if quote["streamer"] == ctx.channel.name]
                    if number > len(quotes):
                        logging.error(f"{number} out of bounds! Only {len(quotes)} quotes found")
                        await ctx.send(f"Argument 'number' out of bounds! Only {len(quotes)} quotes found!" if len(
                            quotes) > 0 else "No quotes found!")
                    else:
                        await ctx.send(format_quote(quotes[number - 1]))
            except Exception as e:
                logging.error(f"{number} is not a valid number. Error message: {str(e)}")
                await ctx.send("Argument 'number' is not a valid number!")
        else:
            await ctx.send(random_quote(ctx))

    @commands.command()
    async def ads(self, ctx: commands.Context):
        # https://github.com/pixeltris/TwitchAdSolutions
        logging.info(f"!ads called by {ctx.author.name}")
        user = ctx.message.author.name
        if user in self._moderators or user == ctx.channel.name:
            if not self._is_command_enabled("ads"):
                await ctx.send("Command disabled by streamer")
                logging.info("Command disabled")
                return
            await ctx.send("https://github.com/pixeltris/TwitchAdSolutions")
        else:
            await ctx.send("<3 you dont have permission to use this command <3")

    @commands.command()
    async def help(self, ctx: commands.Context):
        logging.info(f"!help called by {ctx.author.name}")
        if not self._is_command_enabled("help"):
            await ctx.send("Command disabled by streamer")
            logging.info("Command disabled")
            return
        msg = """Commands:
!help: shows this  ||  
!quote [num]: Shows quote [num] from this streamer. If no number is passed, shows a random quote  ||  
!hello: says hello back  ||  
!ping: Responds with 'Pong!'"""
        if ctx.author.badges.get("vip") or ctx.author.badges.get("mod") or ctx.author.name == ctx.channel.name:
            msg += """  ||  
!addquote [quote] (mods/vips only): Adds a quote. Format as: '!addquote {msg}' without quotation marks"""
        await ctx.send(msg)

    @commands.command(aliases=["so"])
    async def shoutout(self, ctx: commands.Context, streamer: str):
        logging.info(f"!shoutout called by {ctx.author.name} to {streamer}")
        user = ctx.message.author.name
        if user in self._moderators or user == ctx.channel.name:
            if not self._is_command_enabled("shoutout"):
                await ctx.send("Command disabled by streamer")
                logging.info("Command disabled")
                return
            streamer = streamer.strip().replace("@", "")
            user = self._get_user(streamer)
            if user is not None:
                logging.info(f"Streamer ID: {user.id}")
                await ctx.send(f"Go check out @{user.name} at https://twitch.tv/{user.name} !")
                # await user.shoutout(self._token, user.id, self._user.id)
                requests.post(f"https://api.twitch.tv/helix/chat/shoutouts?"
                              f"from_broadcaster_id={self.user_id}&to_broadcaster_id={user.id}"
                              f"&moderator_id={self.user_id}".replace(" ", "").replace("\n", ""),
                              headers={"Authorization": f"Bearer {self._token}",
                                       "Client-Id": self._config["client_id"]}
                              )
                logging.info("Successfully sent shoutout!")
            else:
                logging.error(f"User {streamer} not found!")
                await ctx.send(f"User {streamer} not found!")
        else:
            logging.warning(f"User {ctx.author.name} does not have permission to use !shoutout !")
            await ctx.send("<3 you dont have permission to use this command <3")

    @commands.command()
    async def game(self, ctx: commands.Context):
        user = ctx.message.author.name
        if user in self._moderators or user == ctx.channel.name:
            if not self._is_command_enabled("game"):
                logging.info("Command disabled")
                await ctx.send("Command disabled by streamer")
                return
            try:
                msg = ctx.message.content[ctx.message.content.index(" ") + 1:].strip().replace('"', "")
                logging.info(f"!game called by {ctx.author.name}")
                categories = await self.search_categories(msg)
                if len(categories) > 0:
                    url = f"https://api.twitch.tv/helix/channels?broadcaster_id={self._user.id}"
                    headers = {
                        "Authorization": f"Bearer {self._token}",
                        "Client-Id": self._config["client_id"],
                        "Content-Type": "application/json"
                    }
                    res = requests.patch(url, headers=headers, json={"game_id": categories[0].id})
                    if res.status_code == 204:
                        await ctx.send(f"Successfully updated game to {categories[0].name}")
                    else:
                        logging.error(f"Got status code {res.status_code}")
                else:
                    await ctx.send(f"Game '{msg}' not found")
            except ValueError:
                await ctx.send("Please specify a game!")
        else:
            logging.warning(f"User {ctx.author.name} does not have permission to use !game !")
            await ctx.send("<3 you dont have permission to use this command <3")

    @commands.command()
    async def title(self, ctx: commands.Context):
        user = ctx.message.author.name
        if user in self._moderators or user == ctx.channel.name:
            if not self._is_command_enabled("title"):
                logging.info("Command disabled")
                await ctx.send("Command disabled by streamer")
                return
            try:
                msg = ctx.message.content[ctx.message.content.index(" ") + 1:].strip().replace('"', "")
                logging.info(f"!title called by {ctx.author.name}")
                url = f"https://api.twitch.tv/helix/channels?broadcaster_id={self._user.id}"
                headers = {
                    "Authorization": f"Bearer {self._token}",
                    "Client-Id": self._config["client_id"],
                    "Content-Type": "application/json"
                }
                res = requests.patch(url, headers=headers, json={"title": msg})
                if res.status_code == 204:
                    await ctx.send(f"Successfully updated title to '{msg}'")
                else:
                    logging.error(f"Got status code != 204: {res.status_code}")
            except ValueError:
                await ctx.send("Please specify a title!")
        else:
            logging.warning(f"User {ctx.author.name} does not have permission to use !game !")
            await ctx.send("<3 you dont have permission to use this command <3")

    @commands.command(aliases=("cheat", "cheats"))
    async def cheater(self, ctx: commands.Context):
        logging.info(f"!cheater called by {ctx.message.author.name}")
        if ctx.message.author.name in self._moderators or ctx.message.author.name in self._vips or ctx.author.name == ctx.channel.name:
            if not self._is_command_enabled("cheater"):
                logging.info("Command disabled")
                await ctx.send("Command disabled by streamer")
                return
            try:
                with open("assets/misc_data.json") as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = {"cheats_total": 0}
            data["cheats_total"] += 1
            self._cheated_n_times += 1
            with open("assets/misc_data.json", "w") as file:
                json.dump(data, file, indent=2)
            await ctx.send(
                f"{ctx.channel.name} has cheated {self._cheated_n_times} time(s) this stream ({data['cheats_total']} total)")
        else:
            logging.warning(f"{ctx.message.author.name} does not have permission to use !cheater")
            await ctx.send("<3 you don't have permission to use this command <3")

    @commands.command(aliases=("addcommand", "add_command", "add_cmd"))
    async def addcmd(self, ctx: commands.Context):
        logging.info(f"!add_command called by {ctx.author.name}")
        if ctx.author.name in self._moderators or ctx.author.name == ctx.channel.name:
            if not self._is_command_enabled("add_command"):
                await ctx.send("Command disabled by streamer")
                return
            try:
                msg = ctx.message.content
                cmd_name = msg.split()[1]
                return_ = msg.split()[2:]
                self._misc_data["custom_commands"].append({"name": cmd_name, "return": " ".join(return_), "enabled": True})

                with open("assets/misc_data.json", "w") as file:
                    json.dump(self._misc_data, file, indent=2)

                await ctx.send(f"Successfully added command {cmd_name}")
            except Exception as e:
                logging.error(f"Failed to add command: {str(e)}")
                await ctx.send("Failed to add command")
        else:
            logging.warning(f"{ctx.author.name} does not have permission to add commands")
            await ctx.send("<3 you don't have permission to use this command <3")

    # the (, ) is formatting so Pycharm doesn't freak out
    @commands.command(aliases=("remove_command", ))
    async def remove_cmd(self, ctx: commands.Context):
        logging.info(f"!remove_cmd called by {ctx.author.name}")
        if ctx.author.name in self._moderators or ctx.author.name == ctx.channel.name:
            if not self._is_command_enabled("remove_command"):
                await ctx.send("Command disabled by streamer")
                return
            try:
                msg = ctx.message.content
                cmd_name = msg.lower().split()[1]
                try:
                    cmd = [tmp for tmp in self._misc_data["custom_commands"] if tmp["name"] == cmd_name][0]
                    index = self._misc_data["custom_commands"].index(cmd)
                    self._misc_data["custom_commands"].pop(index)
                except ValueError:
                    pass
                except IndexError:
                    pass

                with open("assets/misc_data.json", "w") as file:
                    json.dump(self._misc_data, file, indent=2)

                    await ctx.send(f"Successfully removed command {cmd_name}")
            except Exception as e:
                logging.error(f"Failed to add command: {str(e)}")
                await ctx.send("Failed to remove command")
        else:
            logging.warning(f"{ctx.author.name} does not have permission to add commands")
            await ctx.send("<3 you don't have permission to use this command <3")

    def disable_command(self, cmd_name):
        default_cmds = self._misc_data["default_commands"]
        custom_cmds = self._misc_data["custom_commands"]
        default_cmd_names = [item["name"] for item in default_cmds]
        custom_cmd_names = [item["name"] for item in custom_cmds]
        try:
            index = default_cmd_names.index(cmd_name)
            self._misc_data["default_commands"][index]["enabled"] = False
        except ValueError:
            try:
                index = custom_cmd_names.index(cmd_name)
                self._misc_data["custom_commands"][index]["enabled"] = False
            except ValueError:
                logging.error("Command not found")
        with open("assets/misc_data.json", "w") as file:
            json.dump(self._misc_data, file, indent=2)
        logging.info(f"Disabled command: {cmd_name}")

    def enable_command(self, cmd_name):
        default_cmds = self._misc_data["default_commands"]
        custom_cmds = self._misc_data["custom_commands"]
        default_cmd_names = [item["name"] for item in default_cmds]
        custom_cmd_names = [item["name"] for item in custom_cmds]
        try:
            index = default_cmd_names.index(cmd_name)
            self._misc_data["default_commands"][index]["enabled"] = True
        except ValueError:
            try:
                index = custom_cmd_names.index(cmd_name)
                self._misc_data["custom_commands"][index]["enabled"] = True
            except ValueError:
                logging.error("Command not found")
        with open("assets/misc_data.json", "w") as file:
            json.dump(self._misc_data, file, indent=2)
        logging.info(f"Disabled command: {cmd_name}")

    def create_poll(self, title: str, options: list, channel_points=False, points_per_vote=0, duration=120):
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Client-Id": self._config["client_id"],
            "Content-Type": "application/json",
        }
        data = {
            "broadcaster_id": self._user.id,
            "title": title,
            "choices": [{"title": option} for option in options],
            "channel_points_voting_enabled": channel_points,
            "channel_points_per_vote": points_per_vote,
            "duration": duration,
        }
        response = requests.post('https://api.twitch.tv/helix/polls', headers=headers, json=data)
        return response.status_code
