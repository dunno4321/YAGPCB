from datetime import datetime, timedelta
from twitchio.ext import commands
from flask import Flask, request
from threading import Thread
import requests
import random
import json
import time

app = Flask(__name__)
has_token = False
token_time = datetime.now() - timedelta(days=3)
token = ""

try:
    with open("config.json") as file:
        config = json.load(file)
except FileNotFoundError:
    print("config.json not found, please run set_stuff.py with the command 'python set_stuff.py'")
tmp = list(config.keys())
tmp.sort()
if tmp != ['channel', 'client_id', 'client_secret']:
    with open("config.json", "w") as file:
        json.dump({"client_id": "", "client_secret": "", "channel": ""}, file, indent=2)
    raise Exception("Invalid config.json format! Resetting to default...")
if config["channel"] == "" or config["client_id"] == "" or config["client_secret"] == "":
    raise Exception("Default config detected, please run set_stuff.py with the command 'python set_stuff.py' to configure the bot")


def parse(url_):
    url_ = url_[url_.rfind("/") + 2:]
    params2 = url_.split("&")
    params = {}
    for item in params2:
        tmp = item.split("=")
        params[tmp[0]] = tmp[1]
    return params


@app.route("/")
def home():
    global token_time, has_token, token
    params = parse(request.url)
    if "code" in list(params.keys()):
        has_token = True
        token = params["code"]
        token_time = datetime.now()
        with open("token.json", "w") as file:
            json.dump({"token": token}, file)
        return "Successfully authorized!"
    else:
        has_token = False
        token = f"error: {params['error']}: {params['error_description']}"
        return token


def add_quote(ctx: commands.Context):
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
    streamer = ctx.channel.name
    with open("quotes.json") as file:
        tmp = json.load(file)
    tmp = [quote for quote in tmp if quote["streamer"] == streamer]
    return format_quote(random.choice(tmp)) if len(tmp) > 0 else "No quotes found for this streamer!"


def get_access_token():
    global has_token
    try:
        with open("token.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        # get a new token, mildly sketchy logic
        data = {"expires_in": datetime.now() - timedelta(days=3)}
    # if the code will expire in less than an hour, get a new one
    if datetime.strptime(data["expires_in"], "%d/%m/%Y %H:%M:%S") < (datetime.now() + timedelta(hours=1)):
        print("Connect to twitch via this link:")
        # print("""https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=28jexim9tw3g8u52evmlqbpob96ymn&redirect_uri=http://localhost:3000&scope=moderator%3Aread%3Achatters%2Bchat%3Aedit%2Bchat%3Aread&state=c3ab8aa609ea11e793ae92361f002671""")
        print(f"""https://id.twitch.tv/oauth2/authorize
        ?response_type=code
        &client_id={config['client_id']}
        &redirect_uri=http://localhost:3000
        &scope=moderator:read:chatters+chat:edit+chat:read""".replace("\n", "").replace(" ", "").strip())
        print("Waiting...")
        while not has_token:
            pass
        response = requests.post("https://id.twitch.tv/oauth2/token", data=f"client_id={config['client_id']}&client_secret={config['client_secret']}&code={token}&grant_type=authorization_code&redirect_uri=http://localhost:3000").json()
        response["expires_in"] = (datetime.now() + timedelta(seconds=response["expires_in"] - 60)).strftime("%d/%m/%Y %H:%M:%S")
        with open("token.json", "w") as file:
            json.dump(response, file)

        return token
    else:
        return data["access_token"]


def refresh_token():
    pass


class Bot(commands.Bot):
    def __init__(self, token, channels=None):
        if channels is None:
            channels = [config['channel']]

        super().__init__(token=token, prefix="!", initial_channels=channels)

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as @{self.nick}')
        print(f'User id is {self.user_id}')
        print(f"Connected to these channels: {[channel.name for channel in self.connected_channels]}")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # cheese
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def ping(self, ctx: commands.Context):
        # pong
        await ctx.send(f'Pong!')

    @commands.command()
    async def addquote(self, ctx: commands.Context):
        # if you see this I'll remove it :]
        if ctx.author.badges.get("vip") or ctx.author.badges.get("mod") or ctx.author.name == "dunno4321" or ctx.author.name == ctx.channel.name:
            num_quotes = add_quote(ctx)
            await ctx.send(f"Successfully added quote #{num_quotes}")
        else:
            await ctx.send("<3 you dont have permission to use this command <3")

    # @commands.command()
    # async def quote(self, ctx: commands.Context):
    #     await ctx.send(random_quote(ctx))

    @commands.command()
    async def quote(self, ctx: commands.Context):
        msg = ctx.message.content.strip().replace("\U000e0000", "")
        args = msg.split(" ")[1:]
        args = [item.strip() for item in args if len(item.strip()) > 0]
        if len(args) != 0:
            number = args[0]
            try:
                number = int(number)
                if number <= 0:
                    await ctx.send("Argument 'number' must be a number greater than 0!")
                else:
                    with open("quotes.json") as file:
                        quotes = json.load(file)
                    quotes = [quote for quote in quotes if quote["streamer"] == ctx.channel.name]
                    if number > len(quotes):
                        await ctx.send(f"Argument 'number' out of bounds! Only {len(quotes)} found!" if len(quotes) > 0 else "No quotes found!")
                    else:
                        await ctx.send(format_quote(quotes[number - 1]))
            except Exception as e:
                print(e)
                await ctx.send("Argument 'number' is not a valid number!")
        else:
            await ctx.send(random_quote(ctx))

    @commands.command()
    async def ads(self, ctx: commands.Context):
        # https://github.com/pixeltris/TwitchAdSolutions
        if ctx.author.badges.get("vip") or ctx.author.badges.get("mod") or ctx.author.name == ctx.channel.name:
            await ctx.send("https://github.com/pixeltris/TwitchAdSolutions")
        else:
            await ctx.send("<3 you dont have permission to use this command <3")

    @commands.command()
    async def help(self, ctx: commands.Context):
        msg = """Commands:     
!help: shows this  ||  
!quote [num]: Shows quote [num] from this streamer. If no number is passed, shows a random quote  ||  
!hello: says hello back  ||  
!ping: Responds with 'Pong!'"""
        if ctx.author.badges.get("vip") or ctx.author.badges.get("mod") or ctx.author.name == ctx.channel.name:
            msg += """  ||  
!addquote [quote] (mods/vips only): Adds a quote. Format as: '!addquote {msg}' without quotation marks  ||  
!ads (mods/vips only): Sends a link to a Github repository with instructions on how to block Twitch ads"""
        await ctx.send(msg)


app_thread = Thread(target=app.run, kwargs={"port": 3000, "host": "0.0.0.0"})
bot = None
try:
    app_thread.start()
    # allow time for the Flask info to get put to console before the link
    time.sleep(0.2)
    token = get_access_token()
    time.sleep(1)
    bot = Bot(token, channels=[config["channel"]])
    print("Attempting connection...")
    bot.run()
except KeyboardInterrupt:
    if bot is not None:
        bot.close()
    app_thread.join(timeout=0)
