from datetime import datetime, timedelta
from twitchio.ext import commands
from flask import Flask, request
from threading import Thread
import requests
import logging
import random
import json
import time

app = Flask(__name__)
has_token = False
token_time = datetime.now() - timedelta(days=3)
token = ""
with open("log.log", "w") as file:
    file.write("")
logging.basicConfig(filename="log.log", level=logging.DEBUG)
logging.info("Hello world!")


def parse(url_):
    logging.debug("Parsing URL: " + url_)
    try:
        url_ = url_[url_.rfind("/") + 2:]
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


@app.route("/")
def home():
    global token_time, has_token, token
    logging.debug("Request on " + request.url)
    params = parse(request.url)
    if "code" in list(params.keys()):
        has_token = True
        token = params["code"]
        token_time = datetime.now()
        with open("token.json", "w") as file:
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


def add_quote(ctx: commands.Context):
    logging.info(f"Adding quote for streamer {ctx.channel.name}")
    with open("quotes.json") as file:
        tmp = json.load(file)
        tmp = [item for item in tmp if item["streamer"] == ctx.channel.name]

    msg = ctx.message.content
    data = {
        "quoter": ctx.message.author.name,
        "msg": msg[msg.find(" ") + 1:],
        "num": len(tmp) + 1,
        "added": datetime.now().strftime("%m/%d/%Y"),
        "streamer": ctx.channel.name
    }

    tmp.append(data)

    with open("quotes.json", "w") as file:
        json.dump(tmp, file)
    return len(tmp)


def format_quote(quote):
    return f"{quote['streamer']} said '{quote['msg']}' on {quote['added']} (#{quote['num']}), as quoted by {quote['quoter']}"


def random_quote(ctx: commands.Context):
    logging.info(f"Getting random quote for streamer {ctx.channel.name}")
    streamer = ctx.channel.name
    with open("quotes.json") as file:
        tmp = json.load(file)
    tmp = [quote for quote in tmp if quote["streamer"] == streamer]
    if len(tmp) == 0:
        logging.warning("No quotes found!")
    return format_quote(random.choice(tmp)) if len(tmp) > 0 else "No quotes found for this streamer!"


def get_access_token(config):
    global has_token
    try:
        logging.info("Attempting to get a previous token...")
        with open("token.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        # get a new token, mildly sketchy logic
        logging.info("token.json not found, creating...")
        data = {"expires_in": datetime.now() - timedelta(days=3)}
    # if the code will expire in less than an hour, get a new one
    if datetime.strptime(data["expires_in"], "%d/%m/%Y %H:%M:%S") < (datetime.now() + timedelta(hours=1)):
        logging.info("Token expired, getting a new one:")
        print("Connect to twitch via this link:")
        scopes = [
            "moderator:read:chatters",
            "chat:edit",
            "chat:read",
            "moderator:manage:shoutouts",
            "channel:manage:polls",
            "moderator:manage:chat_messages",
            "channel:manage:broadcast"
        ]
        logging.info(f"Scopes: {', '.join(scopes)}")
        # print("""https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=28jexim9tw3g8u52evmlqbpob96ymn&redirect_uri=http://localhost:3000&scope=moderator%3Aread%3Achatters%2Bchat%3Aedit%2Bchat%3Aread&state=c3ab8aa609ea11e793ae92361f002671""")
        print(f"""https://id.twitch.tv/oauth2/authorize
        ?response_type=code
        &client_id={config['client_id']}
        &redirect_uri=http://localhost:3000
        &scope={'+'.join(scopes)}""".replace("\n", "").replace(" ", "").strip())
        print("Waiting...")
        logging.info("Waiting for user...")
        while not has_token:
            pass
        response = requests.post("https://id.twitch.tv/oauth2/token",
                                 data=f"client_id={config['client_id']}&client_secret={config['client_secret']}&code={token}&grant_type=authorization_code&redirect_uri=http://localhost:3000").json()
        try:
            response["expires_in"] = (datetime.now() + timedelta(seconds=response["expires_in"] - 60)).strftime(
                "%d/%m/%Y %H:%M:%S")
            with open("token.json", "w") as file:
                json.dump(response, file)

            logging.info(f"New token acquired: {token}")
            return token
        except Exception as e:
            logging.error(f"Error getting token: {str(e)}")
            logging.error("Most likely invalid client id/secret")
            raise Exception(f"Error getting token: {str(e)}. Check your client_id and client_secret in config.json!")
    else:
        return data["access_token"]


class Bot(commands.Bot):
    def __init__(self, config_file, channels=None):
        try:
            with open(config_file) as file:
                config = json.load(file)
        except FileNotFoundError:
            logging.error(f"{config_file} not found!")
            raise Exception(f"{config_file} not found, please run set_stuff.py with the command 'python set_stuff.py'")
        tmp = list(config.keys())
        tmp.sort()
        if tmp != ['channel', 'client_id', 'client_secret']:
            with open(config_file, "w") as file:
                json.dump({"client_id": "", "client_secret": "", "channel": ""}, file, indent=2)
            raise Exception("Invalid config.json format! Resetting to default...")
        if config["channel"] == "" or config["client_id"] == "" or config["client_secret"] == "":
            logging.error("Default config detected, breaking...")
            raise Exception(
                "Default config detected, please run set_stuff.py with the command 'python set_stuff.py' to configure the bot")

        if channels is None:
            channels = [config['channel']]

        self._config = config
        self._token = get_access_token(config)
        print("Attempting connection...")
        logging.info("Attempting connection...")
        # sometimes a new token needs a second to actually work :3
        time.sleep(5)
        super().__init__(token=self._token, prefix="!", initial_channels=channels)
        self._user = self._get_user(config["channel"])
        self._active = True
        self._chatters_checked_at = datetime.now() - timedelta(hours=1)
        # self._thread = Thread(target=self._worker_thread)
        # self._thread.start()

    def _worker_thread(self):
        while self._active:
            now = datetime.now()
            # add chatter points
            if (now - self._chatters_checked_at) > timedelta(minutes=5):
                chatters = self._get(f"https://api.twitch.tv/helix/chat/chatters?broadcaster_id={self._config['channel']}&moderator_id={self.user_id}&first=1000")
                with open("points.json") as file:
                    data = json.load(file)
                # structure: {chatter: points}
                keys = list(data.keys())
                for chatter in chatters:
                    if chatter in keys:
                        data[chatter] += 5
                    else:
                        data[chatter] = 5

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

    async def event_ready(self):
        logging.info(f"Logged in as {self.nick} with ID {self.user_id}")
        logging.info(f"Connected to: {[channel.name for channel in self.connected_channels]}")
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as @{self.nick}')
        print(f'User id is {self.user_id}')
        print(f"Connected to these channels: {[channel.name for channel in self.connected_channels]}")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        logging.info(f"!hello called by {ctx.author.name}")
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def ping(self, ctx: commands.Context):
        logging.info(f"!pong called by {ctx.author.name}")
        # pong
        await ctx.send(f'Pong!')

    @commands.command()
    async def addquote(self, ctx: commands.Context):
        logging.info(f"!addquote called by {ctx.author.name}")
        # if you see this I'll remove it :]
        if ctx.author.badges.get("vip") or ctx.author.badges.get(
                "mod") or ctx.author.name == "dunno4321" or ctx.author.name == ctx.channel.name:
            num_quotes = add_quote(ctx)
            logging.info(f"Added quote #{num_quotes}")
            await ctx.send(f"Successfully added quote #{num_quotes}")
        else:
            logging.info(f"{ctx.author.name} does not have permission to use this command!")
            await ctx.send("<3 you dont have permission to use this command <3")

    @commands.command()
    async def quote(self, ctx: commands.Context):
        logging.info(f"!quote called by {ctx.author.name}")
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
                    with open("quotes.json") as file:
                        quotes = json.load(file)
                    quotes = [quote for quote in quotes if quote["streamer"] == ctx.channel.name]
                    if number > len(quotes):
                        logging.error(f"{number} out of bounds! Only {len(quotes)} found")
                        await ctx.send(f"Argument 'number' out of bounds! Only {len(quotes)} found!" if len(
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
        if ctx.author.badges.get("mod") or ctx.author.name == ctx.channel.name:
            await ctx.send("https://github.com/pixeltris/TwitchAdSolutions")
        else:
            await ctx.send("<3 you dont have permission to use this command <3")

    @commands.command()
    async def help(self, ctx: commands.Context):
        logging.info(f"!help called by {ctx.author.name}")
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
        if ctx.author.badges.get("mod") or ctx.author.name == ctx.channel.name:
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
        try:
            msg = ctx.message.content[ctx.message.content.index(" ") + 1:].strip().replace('"', "")
            logging.info(f"!game called by {ctx.author.name}")
            if ctx.author.badges.get("mod") or ctx.author.name == ctx.channel.name:
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
                    await ctx.send(f"Game '{game}' not found")
            else:
                logging.warning(f"User {ctx.author.name} does not have permission to use !game !")
                await ctx.send("<3 you dont have permission to use this command <3")
        except ValueError:
            await ctx.send("Please specify a game!")

    @commands.command()
    async def title(self, ctx: commands.Context):
        try:
            msg = ctx.message.content[ctx.message.content.index(" ") + 1:].strip().replace('"', "")
            logging.info(f"!title called by {ctx.author.name}")
            if ctx.author.badges.get("mod") or ctx.author.name == ctx.channel.name:
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
            else:
                logging.warning(f"User {ctx.author.name} does not have permission to use !game !")
                await ctx.send("<3 you dont have permission to use this command <3")
        except ValueError:
            await ctx.send("Please specify a title!")


app_thread = Thread(target=app.run, kwargs={"port": 3000, "host": "0.0.0.0"})
bot = None
try:
    logging.info("Starting Flask thread...")
    app_thread.start()
    # allow time for the Flask info to get put to console before the link
    time.sleep(0.2)
    bot = Bot("config.json")
    bot.run()
except KeyboardInterrupt:
    if bot is not None:
        bot.close()
    app_thread.join(timeout=0)
