from datetime import datetime, timedelta
from twitchio.ext import commands
from threading import Thread
import webbrowser
import requests
import twitchio
import logging
import asyncio
import random
import server
import json
import copy
import re

# constants
date_fmt = "%d/%m/%Y"
time_fmt = "%H:%M:%S"
date_time_fmt = date_fmt + " " + time_fmt
eight_ball_responses = ["It is certain", "Don't count on it", "It is decidedly so", "My reply is no", "Without a doubt",
                        "My sources say no", "Yes definitely", "Outlook not so good", "You may rely on it",
                        "Very doubtful", "As I see it, yes", "Most likely", "Outlook promising", "Signs point to yes"]
# TODO: allow changing
raffle_length = 30
raffle_points = 5000
max_winners = 5


def find_all(string, substring):
    return [m.start() for m in re.finditer(substring, string)]


def dump_token(token):
    # token["expires_in"] = (datetime.now() + timedelta(seconds=(int(token["expires_in"]) - 120))).strftime(fmt)
    with open("./assets/token.json", "w") as file:
        json.dump(token, file)


def random_quote(quotes, streamer):
    tmp = [quote for quote in quotes if quote["streamer"] == streamer]
    if len(tmp) == 0:
        logger = logging.getLogger("bot")
        logger.setLevel(logging.DEBUG)
        logger.warning("No quotes found!")
    return format_quote(random.choice(tmp)) if len(tmp) > 0 else "No quotes found for this streamer!"


def format_quote(quote):
    return f"{quote['streamer']} said '{quote['quote']}' on {quote['date']} (#{quote['num']}), as quoted by {quote['quoter']}"


def process_command(msg: twitchio.Message, format: str):
    # assume 'format' has been validated when the command was added
    sender = msg.author.name
    message = msg.content
    channel = msg.channel.name
    args = message.split()[1:]
    with open("./assets/counters.json") as file:
        counters = json.load(file)
    # format constants
    to_return = format.replace("{{by}}", sender).replace("{{channeltime}}",
                                                         datetime.now().strftime("%I:%M %p")).replace("{{streamer}}",
                                                                                                      channel)
    if "{{arg" in to_return:
        needed_args = find_all(to_return, "{{arg")
        tmp = []
        # find all things like {{arg1}}, {{arg2}}
        for index in needed_args:
            tmp2 = to_return[index:]
            tmp.append(tmp2[:tmp2.index("}}")])
        # make list of the unique {{arg[num]}}s (to allow for double {{arg1}} usage and stuff)
        tmp = len(list(set(tmp)))
        if tmp > len(args):
            return f"Invalid number of arguments provided (needed {tmp}, got {len(args)})"
        # replace the args with the provided arguments
        for i in range(len(needed_args)):
            try:
                to_return = to_return.replace("{{arg" + str(i + 1) + "}}", args[i])
            except IndexError:
                pass
    # format the {{random_a_b}} to a random.randint(a, b)
    if "{{random" in to_return:
        while "{{random" in to_return:
            # locate the {{random_a_b}}
            index = to_return.index("{{")
            tmp = to_return[index + 2:]
            tmp = tmp[:tmp.index("}}")]
            tmp = tmp.split("_")
            # get the numbers and the random number
            nums = [int(tmp[1]), int(tmp[2])]
            # random.randint doesn't like it when b > a
            nums.sort()
            num = str(random.randint(nums[0], nums[1]))
            str_ = "{{random_" + str(nums[0]) + "_" + str(nums[1]) + "}}"
            to_return = to_return.replace(str_, num, 1)
    # increment the counters
    if "{{increment" in to_return:
        for index in find_all(to_return, "{{increment"):
            # find
            tmp = to_return[index + 2:]
            key = tmp[:tmp.index("}}")][len("increment") + 1:]
            # increment
            if key.lower() in list(counters.keys()):
                counters[key.lower()] += 1
            else:
                counters[key.lower()] = 1
            # replace
            to_return = to_return.replace("{{increment_" + key + "}}", str(counters[key]))
    # display a counter
    if "{{counter" in to_return:
        for index in find_all(to_return, "{{counter"):
            # find
            tmp = to_return[index + 2:]
            key = tmp[:tmp.index("}}")][len("counter")+1:]
            # get value
            if key.lower() in list(counters.keys()):
                value = counters[key.lower()]
            else:
                value = 0
            # replace
            to_return = to_return.replace("{{counter_"+key+"}}", str(value))
    with open("./assets/counters.json", "w") as file:
        json.dump(counters, file)
    return to_return


def validate_command_syntax(cmd: str):
    if len(find_all(cmd, "{{")) != len(find_all(cmd, "}}")):
        return False, "Amount of {{ != amount of }}"
    if "{{random" in cmd:
        for index in find_all(cmd, "{{random"):
            tmp = cmd[index + 2:]
            tmp = tmp[:tmp.index("}}")].split("_")[1:]
            if len(tmp) != 2:
                return False, "Invalid number of args for {{random_a_b}}"
            try:
                nums = (int(tmp[0]), int(tmp[1]))
                if nums[1] < nums[0]:
                    return False, "Argument 'a' of {{random_a_b}} must be less than argument 'b'"
            except ValueError:
                return False, "Arguments for {{random_a_b}} must be integers!"
    if "{{increment" in cmd:
        for index in find_all(cmd, "{{increment"):
            tmp = cmd[index + 2:]
            tmp = "_".join(tmp[:tmp.index("}}")][len("increment"):].split("_")[1:]).strip()
            if len(tmp) == 0:
                return False, "Missing argument counter_name for {{increment_[counter_name]}}"
    if "{{counter" in cmd:
        for index in find_all(cmd, "{{counter"):
            tmp = cmd[index + 2:]
            tmp = "_".join(tmp[:tmp.index("}}")][len("counter"):].split("_")[1:]).strip()
            if len(tmp) == 0:
                return False, "Missing argument counter_name for {{counter[counter_name]}}"
    return True, "seems legit"


class Bot(commands.Bot):
    default_config = {"client_id": "", "client_secret": "", "channel": ""}
    raffle_participants_ = []
    raffle_winner = ""

    def __init__(self, config_file):
        with open(config_file) as file:
            self._config = json.load(file)
        with open("./assets/token.json") as file:
            self._token_data = json.load(file)
            self._token = None
        with open("./assets/quotes.json") as file:
            self._quotes = json.load(file)
        with open("./assets/watchtime.json") as file:
            self._watchtime = json.load(file)
        self.logger = logging.getLogger("bot")
        self.logger.setLevel(logging.root.getEffectiveLevel())
        self._scopes = [
            "moderator:read:chatters",
            "chat:edit",
            "chat:read",
            "moderator:manage:shoutouts",
            "channel:manage:polls",
            "moderator:manage:chat_messages",
            "channel:manage:broadcast",
            "moderation:read",
            "channel:read:vips",
            "moderator:manage:chat_settings",
            "moderator:manage:announcements",
            "channel:read:subscriptions"
        ]

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        self._running = True
        self._server = server.get_server_instance()
        self._misc_data = self._server.get_data()
        self._token = self._get_token()
        # incase the streamer created a separate user for the bot
        super().__init__(self._token, prefix="!", client_secret=self._config["client_secret"],
                         initial_channels=[self._config["channel"]])
        self._user = None
        self._channel_user = self._get_user(self._config["channel"])
        self._channel = self.get_channel(self._config["channel"])
        self._mods = self._get_mods()
        self._vips = self._get_vips()
        self._last_checked_chatters = datetime.now()
        self._active_raffle = False
        self._raffle_ends_at = None
        self._raffle_participants = []
        self._is_single_raffle = False
        self._active_timers = False
        self._timer_end_times = []
        self._giveaway_data = self._server.get_giveaway_data()
        self.loop.create_task(self._get_subscribers())
        self._thread = Thread(target=self._worker_thread)
        self._thread.start()

    async def event_ready(self):
        self._user = self._get_user(self.nick)
        self.logger.info(f"Logged in as {self.nick} with ID {self.user_id}")
        self.logger.info(f"Connected to: {[channel.name for channel in self.connected_channels]}")
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as @{self.nick}')
        print(f'User id is {self.user_id}')
        print(f"Connected to these channels: {[channel.name for channel in self.connected_channels]}")
        self.logger.info(f"Initial chatters: {self.get_chatters()}")

    async def event_message(self, msg: twitchio.Message):
        content = msg.content
        cmd_name = content.split()[0].replace("!", "").lower()
        if content.startswith("!"):
            matches = [cmd for cmd in self._misc_data["custom_commands"] if cmd["name"].lower() == cmd_name]
            if len(matches) == 0:
                try:
                    self._loop.create_task(self.handle_commands(msg))
                except twitchio.ext.commands.errors.CommandNotFound:
                    self.logger.warning(f"!{cmd_name} not found, probably either removed or another bot")
            else:
                if self._is_command_enabled(matches[0]["name"], False):
                    self._loop.create_task(msg.channel.send(process_command(msg, matches[0]["return"])))
                else:
                    self._loop.create_task(msg.channel.send("command disabled"))

    def _dump_quotes(self):
        with open("./assets/quotes.json", "w") as file:
            json.dump(self._quotes, file)

    def _dump_misc_data(self):
        # deprecated
        with open("./assets/quotes.json", "w") as file:
            json.dump(self._misc_data, file)

    def _dump_watchtime(self):
        with open("./assets/watchtime.json", "w") as file:
            json.dump(self._watchtime, file)

    def _dump_giveaway(self):
        with open("./assets/giveaway.json", "w") as file:
            json.dump(self._giveaway_data, file, indent=2)

    def _get(self, url, **kwargs):
        self.logger.debug(f"Getting url: {url}")
        return requests.get(url, headers={"Authorization": f"Bearer {self._token}",
                                          "Client-Id": self._config["client_id"]}, **kwargs).json()

    def _get_mods(self):
        url = f"https://api.twitch.tv/helix/moderation/moderators?broadcaster_id={self._channel_user.id}"
        res = self._get(url)
        return [user["user_login"] for user in res["data"]]

    def _get_vips(self):
        url = f"https://api.twitch.tv/helix/channels/vips?broadcaster_id={self._channel_user.id}"
        res = self._get(url)
        return [user["user_login"] for user in res["data"]]

    def _get_user(self, username):
        self.logger.debug(f"Attempting to get user {username}")
        try:
            data = self._get(f"https://api.twitch.tv/helix/users?login={username}")["data"][0]
            self.logger.debug(f"Successfully got user {data['display_name']} with ID {data['id']}")
            return self.create_user(data["id"], data["display_name"])
        except IndexError:
            # user does not exist
            self.logger.error(f"User {username} does not exist!")
            return None
        except KeyError:
            self.logger.error("Token not valid ig, wait a few seconds")
            raise Exception("Twitch token being dumb, wait a few seconds then run again")

    # async because there could be a large amount of subs for a streamer
    async def _get_subscribers(self):
        # allow time for the token to be valid
        subs = {}
        params = {"broadcaster_id": str(self._channel_user.id)}
        while True:
            res = self._get("https://api.twitch.tv/helix/subscriptions", params=params)
            for chatter in res["data"]:
                subs["name"] = int(chatter["tier"]) / 1000
            if res["pagination"] == {}:
                break
            else:
                params["after"] = res["pagination"]["cursor"]
        subs[self._channel_user.name] = 3
        self._subs = subs

    def get_chatters(self):
        chatters = []
        params = {"broadcaster_id": str(self._channel_user.id), "moderator_id": str(self._user.id)}
        while True:
            res = self._get("https://api.twitch.tv/helix/chat/chatters", params=params)
            chatters.extend([chatter["user_login"] for chatter in res["data"]])
            if res["pagination"] == {}:
                break
            else:
                params["after"] = res["pagination"]["cursor"]
        return chatters

    def _worker_thread(self):
        while self._running:
            now = datetime.now()

            if (datetime.strptime(self._token_data["expires_in"], date_time_fmt) - now).total_seconds() < 120:
                self.logger.debug("refreshing access token")
                self._token = self._refresh_token()

            self._misc_data = self._server.get_data()
            for task in self._misc_data["repeating_tasks"]:
                # later times are greater
                if datetime.strptime(task["next"], date_time_fmt) < now:
                    self.logger.debug(f"Doing task with data: {task}")
                    if task["type"] == "poll":
                        """
                        poll: {
                            "freq_val": frequency_value,
                            "freq_units": frequency_unit,
                            "title": title,
                            "options": options_text,
                            "c_points_enabled": channel_points_enabled,
                            "c_points_per_vote": channel_points_per_vote,
                            "duration": duration,
                            "next": next,
                            "type": "poll"
                        }
                        """
                        self.create_poll(task["title"], task["options"], task["duration"], task["c_points_enabled"],
                                         task["c_points_per_vote"])
                    else:
                        """
                        msg: {
                            "freq_val": frequency_value,
                            "freq_units": frequency_unit,
                            "msg_body": content,
                            "next": next,
                            "type": "msg"
                        }
                        """
                        self.send_message(task["msg_body"])
                    task["next"] = (now + timedelta(minutes=task["freq_val"])).strftime(date_time_fmt)

            if (now - self._last_checked_chatters).total_seconds() > 60:
                self.loop.create_task(self._get_subscribers())
                self._vips = self._get_vips()
                sub_names = list(self._subs.keys())
                chatters = self.get_chatters()

                with open("assets/watchtime.json") as file:
                    watchtime = json.load(file)
                keys = list(watchtime.keys())
                updated = []
                for chatter in chatters:
                    if chatter in keys:
                        if chatter in sub_names:
                            watchtime[chatter]["points"] += [2, 3, 5][self._subs[chatter] - 1]
                        else:
                            watchtime[chatter]["points"] += 5
                        watchtime[chatter]["watchtime"] += 5
                        updated.append(chatter)
                chatters = [chatter for chatter in chatters if chatter not in updated]
                for chatter in chatters:
                    if chatter in self._subs:
                        watchtime[chatter] = {"watchtime": 5, "points": [2, 3, 5][self._subs[chatter] - 1]}
                    else:
                        watchtime[chatter] = {"watchtime": 5, "points": 1}
                self._watchtime = watchtime
                self._dump_watchtime()
                self._last_checked_chatters = now

            if self._active_raffle and self._raffle_ends_at is not None:
                if self._raffle_ends_at < now:
                    self.logger.info("Raffle over, picking winners...")
                    if self._is_single_raffle:
                        try:
                            winner = random.choice(self._raffle_participants)
                            points = int(raffle_points)

                            if winner in list(self._watchtime.keys()):
                                self._watchtime[winner]["points"] += points
                            else:
                                self._watchtime[winner] = {"points": points, "watchtime": 1}

                            self._dump_watchtime()
                            self.logger.info(f"{winner} won {points} points")
                            self.send_message(f"Raffle over! {winner} won {points} points!")
                        except IndexError:
                            self.send_message("Raffle over! Nobody entered so nobody won!")

                    else:
                        amt_winners = min(random.randint(1, max_winners), len(self._raffle_participants))
                        try:
                            amt_per_winner = int(raffle_points / amt_winners)
                            winners = []

                            for _ in range(amt_winners):
                                tmp = random.choice(self._raffle_participants)
                                winners.append(tmp)
                                self._raffle_participants.pop(self._raffle_participants.index(tmp))

                            for winner in winners:
                                if winner in list(self._watchtime.keys()):
                                    self._watchtime[winner]["points"] += amt_per_winner
                                else:
                                    self._watchtime[winner] = {"points": amt_per_winner, "watchtime": 1}

                            self._dump_watchtime()
                            self.logger.info(f"Raffle over! {', '.join(winners)} each won {amt_per_winner} points!")
                            self.send_message(f"Raffle over! {', '.join(winners)} each won {amt_per_winner} points!")
                        except ZeroDivisionError:
                            self.send_message("Raffle over! Nobody entered so nobody won!")

                    self._active_raffle = False
                    self._raffle_participants = []

            if self._server.get_giveaway_data() is not None or self._server.get_giveaway_data()["active"]:
                self._giveaway_data = self._server.get_giveaway_data()

            if self._server.end_giveaway_:
                data = self._server.giveaway_data
                winner = data["winner"]
                total_entries = 0
                for entry in list(data["entrants"].keys()):
                    total_entries += data["entrants"][entry]
                try:
                    self.send_message(f"{winner} won the giveaway with a {round(100 * (data['entrants'][winner] / total_entries), 2)}% chance of winning! PogChamp")
                except ZeroDivisionError:
                    pass
                self._server.end_giveaway_ = False

            if self._active_timers:
                # avoid stuff from removing items from a list while iterating over it
                tmp = copy.deepcopy(self._timer_end_times)
                for i, data in enumerate(tmp):
                    if now > data[0]:
                        self.logger.info(f"Timer {data[1]} ended")
                        self.send_message(f"Timer {data[1]} is up!")
                        self._timer_end_times = [timer for timer in self._timer_end_times if timer[1] != data[1]]
                self._active_timers = len(self._timer_end_times) > 0

    def _is_command_enabled(self, name, is_default):
        return self._server.is_command_enabled(name, is_default)

    def _get_token(self):
        if self._config == Bot.default_config and self._token_data == {}:
            # no code, no token
            self.logger.debug("Waiting for Flask input...")
            print("Go to http://localhost:3000 to set client_id, client_secret, and channel name!")
            # get config --> get code
            while self._server.get_config() == Bot.default_config and self._server.get_config() != {}:
                pass
            self._config = self._server.get_config()
            with open("./assets/config.json", "w") as file:
                json.dump(self._config, file)
            # multiline url is easier to read :)
            url = f"""https://id.twitch.tv/oauth2/authorize
                        ?response_type=code
                        &client_id={self._config['client_id']}
                        &redirect_uri=http://localhost:3000/token
                        &scope={"+".join(self._scopes)}""".replace("\n", "").replace(" ", "")
            # TODO: keep this or just print link
            # cmd prompt doesn't let you click links
            # i think i'll keep it for now
            self.logger.info(f"Opening browser to {url}")
            print(f"Opening browser to {url}")
            webbrowser.open(url, autoraise=True, new=0)
            while self._server.code is None:
                pass
            code = self._server.code
            res = requests.post("https://id.twitch.tv/oauth2/token",
                                data=f"client_id={self._config['client_id']}&client_secret={self._config['client_secret']}&code={code}&grant_type=authorization_code&redirect_uri=http://localhost:3000/token")
            res.raise_for_status()
            res = res.json()
            res["expires_in"] = (datetime.now() + timedelta(seconds=(res["expires_in"] - 120))).strftime(
                date_time_fmt)
            self._token = res["access_token"]
            self._token_data = res
            dump_token(self._token_data)
            return self._token
            # get code --> get token
        elif self._config != Bot.default_config and self._token_data == {}:
            # have code --> get token
            url = f"""https://id.twitch.tv/oauth2/authorize
                        ?response_type=code
                        &client_id={self._config['client_id']}
                        &redirect_uri=http://localhost:3000/token
                        &scope={"+".join(self._scopes)}""".replace("\n", "").replace(" ", "")
            self.logger.info(f"Opening browser to {url}")
            print(f"Opening browser to {url}")
            webbrowser.open(url, autoraise=True, new=0)

            while self._server.code is None:
                pass
            code = self._server.code

            res = requests.post("https://id.twitch.tv/oauth2/token",
                                data=f"client_id={self._config['client_id']}&client_secret={self._config['client_secret']}&code={code}&grant_type=authorization_code&redirect_uri=http://localhost:3000/token")
            # print(res.text)
            res.raise_for_status()
            res = res.json()
            self._token = res["access_token"]
            res["expires_in"] = (datetime.now() + timedelta(seconds=(res["expires_in"] - 120))).strftime(
                date_time_fmt)
            self._token_data = res
            dump_token(self._token_data)
            return self._token
        elif self._config != Bot.default_config and "code" in list(self._token_data.keys()):
            # no code but config --> get code --> get token
            code = self._token_data["code"]
            res = requests.post("https://id.twitch.tv/oauth2/token",
                                data=f"client_id={self._config['client_id']}&client_secret={self._config['client_secret']}&code={code}&grant_type=authorization_code&redirect_uri=http://localhost:3000/token")
            res.raise_for_status()
            res = res.json()
            res["expires_in"] = (datetime.now() + timedelta(seconds=(res["expires_in"] - 120))).strftime(
                date_time_fmt)
            self._token = res["access_token"]
            self._token_data = res
            dump_token(res)
            return self._token
        elif self._config != Bot.default_config and self._token_data != {}:
            # have past token --> get new token
            return self._refresh_token()

    def _refresh_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = f"grant_type=refresh_token&refresh_token={self._token_data['refresh_token']}&client_id={self._config['client_id']}&client_secret={self._config['client_secret']}"

        res = requests.request("post", "https://id.twitch.tv/oauth2/token", headers=headers, data=data)
        res.raise_for_status()
        res = res.json()
        res["expires_in"] = (datetime.now() + timedelta(seconds=(res["expires_in"] - 120))).strftime(
            date_time_fmt)
        self._token_data = res
        self._token = res["access_token"]
        dump_token(res)
        return res["access_token"]

    def _add_command(self, name, return_):
        self._server.add_command(name, return_, True)

    def _remove_command(self, name):
        self._server.remove_command(name)

    def _enable_command(self, name, is_default):
        self._server.enable_command(name, is_default)

    def _disable_command(self, name, is_default):
        self._server.disable_command(name, is_default)

    def send_announcement(self, msg, color: str | None = None):
        self.logger.info("sending an announcement")
        if not self._running:
            self.logger.error("not running yet lmao")
            raise Exception("cannot invoke send_message because the bot isn't running!")
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Client-Id": self._config["client_id"],
            "Content-Type": "application/json",
        }
        json_ = {
            "message": msg,
            "color": color
        }
        res = requests.post(
            f"https://api.twitch.tv/helix/chat/announcements?broadcaster_id={self._channel_user.id}&moderator_id={self._user.id}",
            headers=headers, json=json_)
        if res.status_code >= 300:
            self.logger.error(f"Failed to create announcement with status code: {res.status_code}")
            print(f"Failed to create announcement with status code: {res.status_code} and text: {res.text}")

    def send_shoutout(self, user):
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Client-Id": self._config["client_id"],
        }

        user = self._get_user(user)
        self.logger.info(f"Shouting out user {user.name} with ID {user.id}")
        url = f"https://api.twitch.tv/helix/chat/shoutouts?from_broadcaster_id={self._channel_user.id}&to_broadcaster_id={user.id}&moderator_id={self._user.id}"
        res = requests.post(url, headers=headers)
        if res.status_code >= 300:
            self.logger.error(f"Failed to create shoutout with status code: {res.status_code} and text {res.text}")
            print(f"Failed to create shoutout with status code: {res.status_code} and text {res.text}")

    def send_message(self, content):
        if self._running:
            if self._channel is None:
                self._channel = self.get_channel(self._config["channel"])
            self._loop.create_task(self._channel.send(content))
        else:
            self.logger.error("not running yet lmao")
            raise Exception("cannot invoke send_message because the bot isn't running!")

    def create_poll(self, title, options, duration=120, channel_points_enabled=False, channel_points_per_vote=100):
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Client-Id": self._config["client_id"],
            "Content-Type": "application/json",
        }
        data = {
            "broadcaster_id": str(self._channel_user.id),
            "title": title,
            "choices": [{"title": option} for option in options],
            "duration": duration,
            "channel_points_voting_enabled": channel_points_enabled,
            "channel_points_per_vote": channel_points_per_vote
        }
        res = requests.post("https://api.twitch.tv/helix/polls", headers=headers, json=data)
        if res.status_code >= 300:
            self.logger.error(f"Failed to create poll with status code: {res.status_code}")
            print(f"Failed to create poll with status code: {res.status_code}")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        self.logger.info(f"!hello called by {ctx.author.name}")
        if self._is_command_enabled("hello", True):
            self._loop.create_task(ctx.send(f"Hello {ctx.author.name}!"))
        else:
            self.logger.info(f"!hello is disabled")
            self._loop.create_task(ctx.send("command disabled"))

    @commands.command()
    async def ping(self, ctx: commands.Context):
        self.logger.info(f"!ping called by {ctx.author.name}")
        if self._is_command_enabled("ping", True):
            self._loop.create_task(ctx.send(f"Pong!"))
        else:
            self.logger.info(f"!ping is disabled")
            self._loop.create_task(ctx.send("command disabled"))

    @commands.command(aliases=("addquote", "aq"))
    async def add_quote(self, ctx: commands.Context):
        name = ctx.author.name
        self.logger.info(f"!addquote called by {name}")
        if name in self._vips or name in self._mods or name == self._channel_user.name:
            if not self._is_command_enabled("addquote", True):
                self.logger.info(f"!addquote is disabled")
                self._loop.create_task(ctx.send("command disabled"))
                return
            msg = ctx.message.content.split()[1:]
            data = {
                "quoter": ctx.author.name,
                "date": datetime.now().strftime(date_fmt),
                "num": len(self._quotes) + 1,
                "quote": " ".join(msg),
                "streamer": self._channel_user.name
            }
            self._quotes.append(data)
            self._dump_quotes()
            self.logger.info(f"added quote {data['num']}")
            self._loop.create_task(ctx.send(f"Added quote #{len(self._quotes)}!"))
        else:
            self.logger.info("user is powerless!")
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command <3"))

    @commands.command(aliases=("q",))
    async def quote(self, ctx: commands.Context):
        self.logger.info(f"!quote called by {ctx.author.name}")
        if not self._is_command_enabled("quote", True):
            self.logger.info(f"!quote is disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        msg = ctx.message.content.split()[1:]
        if len(msg) == 0:
            self._loop.create_task(ctx.send(random_quote(self._quotes, self._config["channel"])))
            return
        else:
            num = msg[0]
            try:
                num = int(num) - 1
                self._loop.create_task(ctx.send(format_quote(self._quotes[num])))
            except ValueError:
                self.logger.error(f"{num} isn't a valid base 10 integer")
                self._loop.create_task(ctx.send("Argument 'number' is invalid!"))
            except IndexError:
                self.logger.error(f"{num} > {len(self._quotes)}!")
                self._loop.create_task(ctx.send(f"Only {len(self._quotes)} quotes found!"))

    @commands.command(aliases=("so",))
    async def shoutout(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!shoutout called by {user}")
        if user in self._mods or user == self._channel_user.name:
            if not self._is_command_enabled("shoutout", True):
                self.logger.info(f"!shoutout is disabled")
                self._loop.create_task(ctx.send("command disabled"))
                return
            try:
                streamer = ctx.message.content.split()[1]
            except IndexError:
                self._loop.create_task(ctx.send("Please specify a streamer to shout out!"))
                return

            streams = await self.fetch_streams(user_logins=[streamer])
            self.send_shoutout(streamer)
            try:
                msg = f"Go check out @{streamer} over at https://twitch.tv/{streamer} ! Last seen playing {streams[0].game_name}"
            except IndexError:
                msg = f"Go check out @{streamer} over at https://twitch.tv/{streamer} !"
            self.send_announcement(msg, color="blue")
        else:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command <3"))

    # add_command is a default twitchio command
    @commands.command(aliases=("addcmd", "add_cmd", "add_command", "addcommand"))
    async def add_command_(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!add_command called by {user}")
        if user in self._mods or user == ctx.channel.name:
            if not self._is_command_enabled("add_command", True):
                self.logger.info("Command disabled")
                self._loop.create_task(ctx.send("command disabled"))
                return
            args = ctx.message.content.split()[1:]
            if len(args) < 2:
                self.logger.info("no return value/name specified")
                self._loop.create_task(ctx.send("Please specify the return value!"))
            else:
                if args[0].lower() not in [cmd["name"].lower() for cmd in self._misc_data["custom_commands"]]:
                    res = validate_command_syntax(ctx.message.content)
                    if res[0]:
                        self._add_command(args[0], " ".join(args[1:]))
                        self._loop.create_task(ctx.send(f"Successfully added command {args[0]}"))
                    else:
                        self._loop.create_task(ctx.send(f"Invalid command syntax: {res[1]}"))
                else:
                    self._loop.create_task(ctx.send(f"Command '!{args[0]}' already exists!"))
        else:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command"))

    # all the ways you could be wrong:
    @commands.command(aliases=("rmvcmd", "rmv_cmd", "remove_cmd", "removecommand", "removecmd"))
    async def remove_command(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!remove_command called by {user}")
        if user in self._mods or user == ctx.channel.name:
            if not self._is_command_enabled("remove_command", True):
                self.logger.info("Command disabled")
                self._loop.create_task(ctx.send("command disabled"))
                return
            args = ctx.message.content.split()[1:]
            if len(args) < 1:
                self.logger.info("no return value/name specified")
                self._loop.create_task(ctx.send("Please specify the return value!"))
            else:
                self._remove_command(args[0])
                self._loop.create_task(ctx.send("Successfully removed command!"))
        else:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command"))

    async def _update_channel_info(self, game=None, language=None, title=None, tags=None, content_labels=None,
                                   content_label_ids=None, content_labels_enabled=None, branded_content=None):
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Client-Id": self._config["client_id"],
            "Content-Type": "application/json",
        }
        params = {
            'broadcaster_id': str(self._channel_user.id),
        }
        data = {}
        if game is not None:
            data["game_id"] = game.id
        if language is not None:
            data["broadcaster_language"] = language
        if title is not None:
            data["title"] = title
        if tags is not None:
            data["tags"] = tags
        if content_labels is not None:
            data["content_classification_labels"] = content_labels
            if content_label_ids is not None:
                data["id"] = content_labels
            if content_labels_enabled is not None:
                data["is_enabled"] = content_labels
        if branded_content is not None:
            data["is_branded_content"] = branded_content
        res = requests.patch('https://api.twitch.tv/helix/channels', params=params, headers=headers, json=data)
        if res.status_code >= 300:
            self.logger.error(f"Failed to update channel config with code {res.status_code}")

    # hehe
    @commands.command(aliases=("tit",))
    async def title(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!title called by {user}")
        if user in self._mods or user == ctx.channel.name:
            if not self._is_command_enabled("title", True):
                self.logger.info("Command disabled")
                self._loop.create_task(ctx.send("command disabled"))
                return
            title = " ".join(ctx.message.content.split()[1:])
            self._loop.create_task(self._update_channel_info(title=title))
            self._loop.create_task(ctx.send(f"Successfully updated title to '{title}'"))
        else:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command"))

    @commands.command()
    async def game(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!game called by {user}")
        if user in self._mods or user == ctx.channel.name:
            if not self._is_command_enabled("game", True):
                self.logger.info("Command disabled")
                self._loop.create_task(ctx.send("command disabled"))
                return
            game = " ".join(ctx.message.content.split()[1:])
            categories = await self.search_categories(game)
            try:
                await self._update_channel_info(game=categories[0])
                name = categories[0].name
                self._loop.create_task(ctx.send(f"Successfully updated game to '{name}'"))
            except IndexError:
                self._loop.create_task(ctx.send(f"nuh uh :3 (game not found)"))
        else:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command"))

    @commands.command(aliases=("wt",))
    async def watchtime(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!watchtime called by {user}")
        if not self._is_command_enabled("watchtime", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        if user in list(self._watchtime.keys()):
            time = self._watchtime[user]["watchtime"]
            hours = int((time - (time % 60)) / 60)
            mins = time % 60
            if hours > 0:
                self._loop.create_task(ctx.send(f"{user} has spent {hours} hours and {mins} minutes watching {self._channel_user.name}"))
            else:
                self._loop.create_task(ctx.send(f"{user} has spent {mins} minutes watching {self._channel_user.name}"))
        else:
            self._loop.create_task(ctx.send(f"{user} has spent 0 minutes watching {self._channel_user.name}"))

    @commands.command(aliases=("p",))
    async def points(self, ctx: commands.Context):
        user = ctx.message.author.name.lower()
        msg = ctx.message.content.split()[1:]
        self.logger.info(f"!points called by {user}")
        if not self._is_command_enabled("points", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        if len(msg) != 0:
            user = msg[0].replace("@", "").lower()
            if user in list(self._watchtime.keys()):
                sorted_ = sorted(self._watchtime, key=lambda item: self._watchtime[item]["points"], reverse=True)
                pos = sorted_.index(user)
                self._loop.create_task(ctx.send(f"{user} has {self._watchtime[user]['points']} points (#{pos+1}/{len(sorted_)})"))
            else:
                self._loop.create_task(ctx.send(f"{user} not found"))
        else:
            if user in list(self._watchtime.keys()):
                sorted_ = sorted(self._watchtime, key=lambda item: self._watchtime[item]["points"], reverse=True)
                pos = sorted_.index(user)
                self._loop.create_task(ctx.send(f"{user} has {self._watchtime[user]['points']} points (#{pos+1}/{len(sorted_)})"))
            else:
                self._loop.create_task(ctx.send(f"{user} not found"))

    @commands.command()
    async def gamble(self, ctx: commands.Context):
        user = ctx.message.author.name
        multipliers = [0, 0, 0, 0, 0, 2, 2, 2, 3, 3, 3, 5, 5]
        self.logger.info(f"!points called by {user}")
        if not self._is_command_enabled("points", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        msg = ctx.message.content.split()
        if len(msg) == 1:
            self._loop.create_task(ctx.send("Please specify an amount to gamble!"))
            return
        if user in list(self._watchtime.keys()):
            try:
                points = self._watchtime[user]["points"]
                if msg[1].lower() == "all":
                    amt = points
                else:
                    amt = int(msg[1])
                if amt > points:
                    self._loop.create_task(ctx.send(f"You only have {points} points to gamble!"))
                    return
                points -= amt
                won = amt * random.choice(multipliers)
                points += won
                self._watchtime[user]["points"] = points
                self._dump_watchtime()
                if won == 0:
                    self._loop.create_task(ctx.send(
                        f"{user} gambled {amt} points and lost them all, resulting in {points} remaining points"))
                else:
                    self._loop.create_task(ctx.send(
                        f"{user} gambled {amt} points and won {won} points, resulting in {points} points total"))
            except ValueError:
                self._loop.create_task(ctx.send(f"'{msg[1]}' is not a valid integer!"))
        else:
            self._loop.create_task(ctx.send(f"{user} has no points to gamble!"))

    @commands.command(aliases=("gp", "give_points"))
    async def givepoints(self, ctx: commands.Context):
        user = ctx.message.author.name.replace("@", "").lower()
        self.logger.info(f"!givepoints called by {user}")
        if not self._is_command_enabled("givepoints", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        msg = ctx.message.content.split()
        if len(msg) == 1:
            self._loop.create_task(ctx.send("Please specify someone to give the points to!"))
            return
        if len(msg) == 2:
            self._loop.create_task(ctx.send("Please specify an amount of points to give!"))
            return
        if user in list(self._watchtime.keys()):
            points = self._watchtime[user]["points"]
            user_ = msg[1].replace("@", "").lower()
            amt = msg[2]
            try:
                if amt.lower() == "all":
                    amt = points
                else:
                    amt = int(amt)
                if amt > points:
                    self._loop.create_task(ctx.send(f"You only have {points} points to give!"))
                    return
                if amt == 0:
                    self._loop.create_task(ctx.send("Cannot give 0 points!"))
                    return
                if user_.lower() in list(self._watchtime.keys()):
                    self._watchtime[user_.lower()]["points"] += amt
                else:
                    self._watchtime[user_.lower()] = {"watchtime": 1, "points": amt}
                self._watchtime[user]["points"] -= amt
                self._dump_watchtime()
                self._loop.create_task(ctx.send(f"Successfully gave {user_} {amt} points"))
            except ValueError:
                self._loop.create_task(ctx.send(f"{amt} is not a valid integer!"))
        else:
            self._loop.create_task(ctx.send(f"{user} has no points to give!"))

    @commands.command(aliases=("mgp", "mod_give_points"))
    async def modgivepoints(self, ctx: commands.Context):
        user = ctx.message.author.name.replace("@", "").lower()
        self.logger.info(f"!givepoints called by {user}")
        if not self._is_command_enabled("givepoints", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        if user not in self._mods and user != self._channel_user.name.lower():
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command <3"))
            return
        msg = ctx.message.content.split()
        if len(msg) == 1:
            self._loop.create_task(ctx.send("Please specify someone to give the points to!"))
            return
        if len(msg) == 2:
            self._loop.create_task(ctx.send("Please specify an amount of points to give!"))
            return
        user_ = msg[1].replace("@", "").lower()
        amt = msg[2]
        try:
            amt = int(amt)
            if amt == 0:
                self._loop.create_task(ctx.send("Cannot give 0 points!"))
                return
            if user_.lower() in list(self._watchtime.keys()):
                self._watchtime[user_.lower()]["points"] += amt
            else:
                self._watchtime[user_.lower()] = {"watchtime": 1, "points": amt}
            self._dump_watchtime()
            self._loop.create_task(ctx.send(f"Successfully gave {user_} {amt} points"))
        except ValueError:
            self._loop.create_task(ctx.send(f"{amt} is not a valid integer!"))

    @commands.command(aliases=("cf", "flip"))
    async def coinflip(self, ctx: commands.Context):
        user = ctx.message.author.name
        multipliers = [0, 2]
        self.logger.info(f"!coinflip called by {user}")
        if not self._is_command_enabled("coinflip", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        msg = ctx.message.content.split()
        if len(msg) == 1:
            self._loop.create_task(ctx.send("Please specify an amount to gamble!"))
            return
        if user in list(self._watchtime.keys()):
            try:
                points = self._watchtime[user]["points"]
                if msg[1].lower() == "all":
                    amt = points
                else:
                    amt = int(msg[1])
                if amt > points:
                    self._loop.create_task(ctx.send(f"You only have {points} points to gamble!"))
                    return
                points -= amt
                won = amt * random.choice(multipliers)
                points += won
                self._watchtime[user]["points"] = points
                self._dump_watchtime()
                if won == 0:
                    self._loop.create_task(ctx.send(
                        f"{user} gambled {amt} points and lost them all, resulting in {points} remaining points"))
                else:
                    self._loop.create_task(ctx.send(
                        f"{user} gambled {amt} points and won, resulting in {points} points total"))
            except ValueError:
                self._loop.create_task(ctx.send(f"{msg[1]} is not a valid integer!"))
        else:
            self._loop.create_task(ctx.send(f"{user} has no points to gamble!"))

    @commands.command(aliases=("tp", "take_points"))
    async def takepoints(self, ctx: commands.Context):
        user = ctx.message.author.name.replace("@", "").lower()
        self.logger.info(f"!takepoints called by {user}")
        if not self._is_command_enabled("takepoints", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        if user not in self._mods and user != ctx.channel.name:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command <3"))
            return
        msg = ctx.message.content.split()
        if len(msg) == 1:
            self._loop.create_task(ctx.send("Please specify someone to take the points from!"))
            return
        if len(msg) == 2:
            self._loop.create_task(ctx.send("Please specify an amount of points to take!"))
            return
        points = self._watchtime[user]["points"]
        user_ = msg[1]
        amt = msg[2]
        try:
            if amt == "all":
                amt = points
            else:
                amt = int(amt)
            if amt == 0:
                self._loop.create_task(ctx.send("Cannot take 0 points!"))
                return
            if user_ in list(self._watchtime.keys()):
                self._watchtime[user_]["points"] -= amt
            else:
                self._watchtime[user_] = {"watchtime": 1, "points": -amt}
            self._dump_watchtime()
            self._loop.create_task(ctx.send(f"{user_} now has {self._watchtime[user_]['points']} points."))
        except ValueError:
            self._loop.create_task(ctx.send(f"{amt} is not a valid integer!"))

    @commands.command(aliases=("lb",))
    async def leaderboard(self, ctx: commands.Context):
        user = ctx.message.author.name.lower()
        self.logger.info(f"!leaderboard called by {user}")
        if not self._is_command_enabled("leaderboard", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        leaders = sorted(self._watchtime, key=lambda item: self._watchtime[item]["points"], reverse=True)[:5]
        # yay one-liners
        builder = ", ".join(f"#{leaders.index(leader)+1}: {leader} with {self._watchtime[leader]['points']} points" for leader in leaders)
        self.logger.debug("leaderboard string: " + builder)
        self._loop.create_task(ctx.send("Points leaderboard: " + builder))

    @commands.command()
    async def love(self, ctx: commands.Context):
        user = ctx.message.author.name.replace("@", "").lower()
        msg = ctx.message.content.split()[1:]
        self.logger.info(f"!love called by {user}")
        if not self._is_command_enabled("love", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        if len(msg) == 0:
            self.logger.warning("No argument specified")
            self._loop.create_task(ctx.send("Please specify something you would like to love"))
            return
        self._loop.create_task(ctx.send(f"There is {random.randint(0, 100)}% love detected between {user} and {msg[0]} <3"))

    @commands.command(aliases=("8ball",))
    async def eightball(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!8ball called by {user}")
        if not self._is_command_enabled("8ball", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        self._loop.create_task(ctx.send(random.choice(eight_ball_responses)))

    @commands.command()
    async def syntax(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!syntax called by {user}")
        if user in self._mods or user == ctx.channel.name:
            if not self._is_command_enabled("syntax", True):
                self.logger.info("Command disabled")
                self._loop.create_task(ctx.send("command disabled"))
                return
            self._loop.create_task(ctx.send("{{by}} --> person who sent the message. {{arg1}}, {{arg2}} --> replaces with the arguments after the !{{command}}. {{random_a_b}} --> random int in [a, b]. {{channeltime}} --> streamer's local time. {{increment_[counter_name]}} --> increments and replaces with a counter. {{counter_[counter_name]}} --> just the value of the counter. {{streamer}} --> channel name. Things like {{increment_bonk_{{arg1}}}} also work"))
        else:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command <3"))

    @commands.command()
    async def raffle(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!raffle called by {user}")
        if user not in self._mods and user != self._channel_user.name:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command <3"))
            return
        if not self._is_command_enabled("raffle", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        if self._active_raffle:
            self.logger.info("There is already an active raffle!")
            self._loop.create_task(ctx.send("There is already an active raffle!"))
            return
        self.logger.info(f"New raffle started for {raffle_points} points")
        self._raffle_ends_at = datetime.now() + timedelta(seconds=raffle_length)
        self._active_raffle = True
        self._is_single_raffle = False
        self._raffle_participants = []
        self._loop.create_task(ctx.send(f"New Multi-Raffle for {raffle_points} points! Type !join to join! Ends in 30 seconds! PogChamp"))

    @commands.command(aliases=("cr", "cancel_raffle"))
    async def cancelraffle(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!cancelraffle called by {user}")
        if user not in self._mods and user != self._channel_user.name:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command <3"))
            return
        if not self._is_command_enabled("cancelraffle", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        self.logger.info(f"Cancelled currently active raffle")
        self._active_raffle = False
        self._is_single_raffle = False
        self._raffle_participants = []
        self._loop.create_task(ctx.send(f"Raffle cancelled"))

    @commands.command()
    async def join(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!join called by {user}")
        if not self._is_command_enabled("join", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        if self._active_raffle and user not in self._raffle_participants:
            self._raffle_participants.append(user)
        elif not self._active_raffle:
            self._loop.create_task(ctx.send("No active raffle found!"))

    @commands.command(aliases=("singleraffle", "single_raffle"))
    async def sraffle(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!sraffle called by {user}")
        if user not in self._mods and user != self._channel_user.name:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command <3"))
            return
        if not self._is_command_enabled("sraffle", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        self.logger.info(f"New raffle started for {raffle_points} points")
        self._active_raffle = True
        self._is_single_raffle = True
        self._raffle_participants = []
        self._raffle_ends_at = datetime.now() + timedelta(seconds=raffle_length)
        self._loop.create_task(ctx.send(f"New Single-Raffle for {raffle_points} points! Type !join to join! PogChamp"))

    @commands.command()
    async def giveaway(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!giveaway called by {user}")
        if not self._is_command_enabled("giveaway", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        if self._giveaway_data is None or self._giveaway_data == {} or not self._giveaway_data["active"]:
            self.logger.info("No active giveaway found!")
            self._loop.create_task(ctx.send("No active giveaway found!"))
            return
        self._loop.create_task(ctx.send(self._giveaway_data["description"]))

    @commands.command(aliases=("ticket",))
    async def enter(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!enter called by {user}")
        if not self._is_command_enabled("enter", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
        if self._giveaway_data is None or self._giveaway_data == {} or not self._giveaway_data["active"]:
            self.logger.info("No active giveaway found!")
            self._loop.create_task(ctx.send("No active giveaway found!"))
            return
        msg = ctx.message.content.lower().split()[1:]
        if len(msg) == 0:
            self._loop.create_task(ctx.send("Please specify an amount of tickets to buy!"))
            return
        if user not in list(self._watchtime.keys()):
            self._loop.create_task(ctx.send("You don't have any points!"))
            return
        user_points = self._watchtime[user]["points"]
        ticket_cost = self._giveaway_data["ticket_cost"]
        if user_points < ticket_cost:
            self._loop.create_task(ctx.send("Cannot afford any tickets!"))
            return
        try:
            if msg[0] == "max":
                tickets = (user_points - (user_points % ticket_cost)) / ticket_cost
            else:
                tickets = int(msg[0])
                if tickets <= 0:
                    self._loop.create_task(ctx.send("You must specify an amount of tickets greater than 0!"))
                max_tickets = (user_points - (user_points % ticket_cost)) / ticket_cost
                if max_tickets < tickets:
                    self._loop.create_task(ctx.send(f"You can only afford {int(max_tickets)} tickets!"))
                    return
        except ValueError:
            self._loop.create_task(ctx.send("Invalid value for argument 'number'"))
            return
        tickets = int(tickets)
        self._watchtime[user]["points"] -= (tickets * ticket_cost)
        if user in list(self._giveaway_data["entrants"].keys()):
            self._giveaway_data["entrants"][user] += tickets
        else:
            self._giveaway_data["entrants"][user] = tickets
        self._dump_giveaway()
        self._dump_watchtime()
        self._loop.create_task(ctx.send(f"Successfully purchased {tickets} tickets for a total of {int(self._giveaway_data['entrants'][user])} tickets"))

    @commands.command()
    async def timer(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!timer called by {user}")
        if user not in self._mods and user != ctx.channel.name:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command <3"))
            return
        if not self._is_command_enabled("timer", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        time = ctx.message.content.split()[1:]
        if len(time) == 0:
            self.logger.info("length of time needed")
            self._loop.create_task(ctx.send("Please specify an length of time!"))
            return
        time = time[0]
        try:
            time = int(time)
            if time <= 0:
                self.logger.info("time <= 0")
                self._loop.create_task(ctx.send("'time' argument must be > 0"))
                return
            self._active_timers = True
            timer_num = 0
            while True:
                if timer_num not in [timer[1] for timer in self._timer_end_times]:
                    break
                timer_num += 1
            self._timer_end_times.append((datetime.now() + timedelta(minutes=time), timer_num))
            self.logger.info(f"Created a {time} minute timer (#{timer_num})!")
            self._loop.create_task(ctx.send(f"Created a {time} minute timer (timer #{timer_num})!"))
        except ValueError:
            self.logger.info(f"Invalid value for arg 'time': {time}")
            self._loop.create_task(ctx.send("Invalid value for argument 'time'"))
            return

    @commands.command(aliases=("canceltimer", "cts", "ct", "cancel_timer", "cancel_timers"))
    async def canceltimers(self, ctx: commands.Context):
        user = ctx.message.author.name
        self.logger.info(f"!canceltimers called by {user}")
        if user not in self._mods and user != ctx.channel.name:
            self._loop.create_task(ctx.send("<3 you don't have permission to use this command <3"))
            return
        if not self._is_command_enabled("canceltimers", True):
            self.logger.info("Command disabled")
            self._loop.create_task(ctx.send("command disabled"))
            return
        self._active_timers = False
        tmp = len(self._timer_end_times)
        self._timer_end_times = []
        if tmp > 0:
            self._loop.create_task(ctx.send("Cancelled all running timers"))
        else:
            self._loop.create_task(ctx.send("No running timers found!"))
