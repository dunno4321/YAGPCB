# YAGP(T)CB!
#### Yet another general purpose Twitch chatbot made by dunno4321. For questions, DM @dunno4321 on Discord


## Installation
You can either follow these steps to build & run it OR go to the Releases tab and download YAGPCBv2-1.exe and follow the instructions there
1. Download and install this by clicking (on GitHub) code --> download ZIP, and extract it to a known location
2. [Install Python](https://www.digitalocean.com/community/tutorials/install-python-windows-10)
3. [Install PIP](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/#). It should install with Python, but it's better to check
4. Open File Explorer and navigate to this folder
5. In the address bar, type "cmd"
6. Type "python -m pip install -r requirements.txt" into Command Prompt. This will install the required libraries
    - If it returns something like "python is not recognized as a...", try running just `python` and install it from the Microsoft Store
7. When that has finished installing, follow [these steps](https://dev.twitch.tv/docs/authentication/register-app/) to create & register a bot and take note of your `client_id` and your `client_secret`
8. Set "OAuth Redirect URL" to "https://localhost:3000/token"
9. To connect with twitch, run the bot with `python main.py` and navigate to [https://localhost:3000](https://localhost:3000) in your web browser
10. Enter the client id, secret, and your channel name. All of this data is stored locally in assets/config.json and only in assets/config.json

## Running the bot
1. Open this folder in File Explorer
2. Type "cmd" into the address bar
3. Type `python main.py` into the command prompt
4. It will ask you to click the link to authorize the bot with Twitch
5. Click the link and follow the instructions to authorize the bot
6. When you are done, you might see an error in command prompt about a JSON parse error. This is normal, no I don't know why it does that, just close command prompt and rerun the bot
7. The bot should connect and print some debug info about the username and user ID of the bot.
8. You should now be able to type !ping into your chat and have the bot respond with Pong!
9. If something doesn't work, go to assets/log.log and do a ctrl+F for "error" or DM me on Discord @dunno4321 with the log file
10. The web dashboard is located at [https://localhost:3000](https://localhost:3000)

## Commands

### !addquote [quote] (VIPs/Mods only)
- Adds a quote to the database. Stores quoter name, message, and date/time added
- All data can be found in the quotes.json file
- Syntax: `!addquote [quote]`
- Aliases: !add_quote, !aq

### !quote [num] (anyone)
- Displays quote [num] from the channel as follows:
- ```"{streamer} said '{msg}' on {added} (#{num}), as quoted by {quoter}"```
- e.x. "dunno4321 said 'test1' on 10/13/23 (#1), as quoted by dunno4321"
- If nothing is provided for [num], picks and displays a random quote
- Syntax: `!quote [num]`
- Aliases: !q

### !hello (anyone)
- Says hello back!

### !ping (anyone)
- Responds with Pong!

### !shoutout [user] (Mods only)
- Shouts out a user
- Syntax: `!shoutout [user]`
- Aliases: !so

### !title [title] (Mods only)
- Sets the stream title
- Syntax: `!title [title]`

### !game [game] (Mods only)
- Sets the game Twitch displays
- Syntax: `!game [game]`

### !add_command [command] [return] (Mods only)
- Adds a custom command that will put [return] in chat when called
- Syntax: `!addcmd [command] [return]`
- Example:
  - > `!addcmd twitter follow me on twitter @dunno4321`
  - > `Successfully added command!`
  - > `!twitter`
  - > `follow me on twitter @dunno4321`
- Advanced command syntax:
- {{by}} --> chatter that sent the message
- {{arg1}}, {{arg2}} --> arguments provided in the message calling the command
- {{random_a_b}} --> random number from a to b, inclusive
- {{channeltime}} --> channel local time
- {{increment_[counter]}} --> increments a counter. Things like {{increment_bonk_{{arg1}}}} also work
- {{counter_[counter]}} --> displays a counter. Things like {{counter_bonk_{{arg1}}}} also work
- {{streamer}} --> channel name
- Examples:
- `!addcmd bonk {{by}} bonks {{arg1}}. ({{arg1}} has been bonked {{increment_bonk_{{arg1}}}} times)`
  -  > somedude: !bonk dunno4321
  -  > somedude bonks dunno4321 (dunno4321 has been bonked 1 times)
  -  > somedude: !bonk dunno4321
  -  > somedude bonks dunno4321 (dunno4321 has been bonked 2 times)
  -  > somedude: !bonk thestreamer
  -  > somedude bonks thestreamer (thestreamer has been bonked 1 times)
- `!addcmd time it is currently {{channeltime}} for {{streamer}}`
  - > somedude: !time
  - > it is currently 02:30 PM for dunno4321
- `!addcmd nerd {{by}} challenges {{arg1}} to a quick math battle: first to solve {{random_10_100}}*{{random_10_100}} wins!`
  - > somedude: !nerd dunno4321
  - > somedude challenges dunno4321 to a quick math battle: first to solve 67*94 wins!
- Aliases: !addcmd, !add_cmd, !addcommand

### !remove_command [command] (Mods only)
- Removes a custom command
- Syntax: `!remove_command [command]`
- Example:
  - > `!remove_command twitter`
  - > `Succesfully removed command twitter`
- Aliases: !remove_cmd, !removecmd, !rmvcmd, !rmv_cmd, !removecommand, !remove_cmd

## !watchtime
- Gives the watchtime of the chatter since the bot was implemented
- Syntax: `!watchtime`
- Example:
  - > `somedude: !watchtime`
  - > `somedude has spent 23 minutes watching dunno4321`
  - > `someotherdude: !watchtime`
  - > `someotherdude has spent 2 hours and 49 minutes watching dunno4321`
- Aliases: !wt

## !love [item]
- Calculates the love between the chatter and [item]
- Syntax: `!love [item]`
- Example:
  - > `somedude: !love cheese`
  - > `There is 69% love detected between somedude and cheese <3`
  - > `someotherdude: !love chatting`
  - > `There is 3% love detected between someotherdude and chatting <3`
- Aliases: !wt

## !8ball [question]
- Consult the 8ball!
- Syntax: `!8ball [question]`
- Example:
  - > `somedude: !8ball should i go to sleep`
  - > `My sources say no`
  - > `someotherdude: !8ball should I use my twitch prime on this streamer`
  - > `Without a doubt`
- Aliases: !eightball

## !syntax (Mods only)
- Gives the syntax on how to add an advanced custom command
- Syntax: `!syntax`
- Example:
  - > `agoodmod: !syntax`
  - > `{{by}} --> person who sent the message. {{arg1}}, {{arg2}} --> replaces with the arguments after the !{{command}}. {{random_a_b}} --> random int in [a, b]. {{channeltime}} --> streamer's local time. {{increment[counter_name]}} --> increments and replaces with a counter. {{counter_[counter_name]}} --> just the value of the counter. {{streamer}} --> channel name. Things like {{increment_bonk_{{arg1}}}} also work`
- Aliases: none

### Web dashboard
- Go to [http://localhost:3000](http://localhost:3000) for the web configuration
- Options:
  - Set client id, secret, and channel
  - ![img.png](readme_pics/img.png)
  - add/remove repeating messages/polls
    - ![img_1.png](readme_pics/img_1.png)
    - ![img_2.png](readme_pics/img_2.png)
  - enable/disable default commands
    - ![img_3.png](readme_pics/img_3.png)
  - enable/disable custom commands
  - ![img_4.png](readme_pics/img_4.png)

## Debugging
- Check log.log (do a ctrl+f for "error") and/or DM me on Discord with the log file

## Todos:
- Web UI for configuration (done)
  - Move Flask app inside of bot.py to be run with bot.Bot (done)
- Option for auto polls like "is audio good?" (done)
