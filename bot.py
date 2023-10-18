from datetime import datetime, timedelta
from twitchio.ext import commands
import requests
import logging
import random
import json
import time


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
        json.dump(tmp, file)
    return len(tmp)


class Bot(commands.Bot):
    # TODO: update token in twitchio
    def __init__(self, config_file, token_callback, channels=None):
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
        self.has_token = False
        self._token = self.get_access_token(token_callback)
        print("Attempting connection...")
        logging.info("Attempting connection...")
        # sometimes a new token needs a second to actually work :3
        time.sleep(5)
        super().__init__(token=self._token, prefix="!", initial_channels=channels, client_secret=config["client_secret"])
        self._user = self._get_user(config["channel"])
        self._active = True
        self._token_data = None
        self._chatters_checked_at = datetime.now() - timedelta(hours=1)
        # self._thread = Thread(target=self._worker_thread)
        # self._thread.start()

    def refresh_token(self):
        logging.info("Refreshing access token...")
        response = requests.post("https://id.twitch.tv/oauth2/token",
                                 headers={"Content-Type": "application/x-www-form-urlencoded"},
                                 data=f"grant_type=refresh_token&refresh_token={self._token_data['refresh_token']}&client_id={self._config['client_id']}&client_secret={self._config['client_secret']}")
        if response.status_code >= 400:
            print(f"Failed to refresh token (HTTP code {response.status_code}, https://http.cat/{response.status_code}")
            logging.error(f"Failed to refresh token (HTTP code {response.status_code}, https://http.cat/{response.status_code}")
        else:
            data = response.json()
            self._token_data["access_token"] = data["access_token"]
            self._token_data["refresh_token"] = data["refresh_token"]
            self._token_data["expires_in"] = (datetime.now() + timedelta(hours=3.5)).strftime("%d/%m/%Y %H:%M:%S")
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
            data = {}
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
                "channel:manage:broadcast"
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
            while callback() is None:
                pass
            token = callback()
            response = requests.post("https://id.twitch.tv/oauth2/token",
                                     data=f"client_id={self._config['client_id']}&client_secret={self._config['client_secret']}&code={token}&grant_type=authorization_code&redirect_uri=http://localhost:3000/token").json()
            try:
                response["expires_in"] = (datetime.now() + timedelta(seconds=response["expires_in"] - 60))
                self._token_data = response
                response["expires_in"] = response["expires_in"].strftime("%d/%m/%Y %H:%M:%S")
                with open("assets/token.json", "w") as file:
                    json.dump(response, file)

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
            if abs((now - self._token_data["expires_in"]).total_seconds()) < 120:
                self.refresh_token()

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

    @commands.command()
    async def hello(self, ctx: commands.Context):
        logging.info(f"!hello called by {ctx.author.name}")
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def ping(self, ctx: commands.Context):
        logging.info(f"!ping called by {ctx.author.name}")
        # pong
        await ctx.send(f'Pong!')

    @commands.command()
    async def addquote(self, ctx: commands.Context):
        logging.info(f"!addquote called by {ctx.author.name}")
        if ctx.author.badges.get("vip") or ctx.author.badges.get(
                "mod") or ctx.author.name == ctx.channel.name:
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
                    with open("assets/quotes.json") as file:
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
                    await ctx.send(f"Game '{msg}' not found")
            else:
                logging.warning(f"User {ctx.author.name} does not have permission to use !game !")
                await ctx.send("<3 you dont have permission to use this command <3")
        except ValueError:
            await ctx.send("Please specify a game!")

    @commands.command()
    async def title(self, ctx: commands.Context):
        if ctx.author.badges.get("mod") or ctx.author.name == ctx.channel.name:
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
