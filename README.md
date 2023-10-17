# YAGPTCB!
#### Yet another general purpose Twitch chatbot made by dunno4321. For questions, DM @dunno4321 on Discord


## Installation
1. Download and install this by clicking (on GitHub) code --> download ZIP, and extract it to a known location
2. [Install Python](https://www.python.org/downloads/release/python-3100/)
3. [Install PIP](https://pip.pypa.io/en/stable/installation/). It should install with Python, but it's better to check
4. Open File Explorer and navigate to this folder
5. In the address bar, type "cmd"
6. Type "python -m pip install -r requirements.txt" into Command Prompt. This will install the required libraries
    - If it returns something like "python is not recognized as a...", try "C:\Users\\<User>\AppData\Local\Programs\Python\Python310\python.exe set_stuff.py" and use that instead of "python ..."
7. When that has finished installing, follow [these steps](https://dev.twitch.tv/docs/authentication/register-app/) to create & register a bot and take note of your `client_id` and your `client secret`
8. Set "OAuth Redirect URL" to "http://localhost:3000"
9. In the command window opened above, type `python set_stuff.py` to start to configuration wizard
    - If it returns something like "python is not recognized as a...", try "C:\Users\\<User>\AppData\Local\Programs\Python\Python310\python.exe set_stuff.py" and use that instead of "python ..."
10. Enter the client id, secret, and your channel name. All of this data is stored locally in config.json and only in config.json

## Running the bot
1. Open this folder in File Explorer
2. Type "cmd" into the address bar
3. Type `python main.py` into the command prompt
4. It will ask you to click the link to authorize the bot with Twitch
5. Click the link and follow the instructions
6. When you are done, you should see a "Successfully authorized!" message and you can close the tab. If not, DM me on Discord (@dunno4321) with a screenshot of the error and a copy of the program output
7. The bot should now connect to Twitch and be in your chat. To test this, you should be able to type "!ping" and have the bot respond with "Pong!"
8. The bot will also print some info once it is connected (username, user id, and which channel it is connected to)
9. See Commands for usage
10. To stop the bot, press ctrl+C twice or close Command Prompt

## Commands

### !addquote [quote] (VIPs/Mods only)
- Adds a quote to the database. Stores quoter name, message, and date/time added
- All data can be found in the quotes.json file
- Syntax: !addquote [quote]

### !quote [num] (anyone)
- Displays quote [num] from the channel as follows:
- ```"{streamer} said '{msg}' on {added} (#{num}), as quoted by {quoter}"```
- e.x. "dunno4321 said 'test1' on 10/13/23 (#1), as quoted by dunno4321"
- If nothing is provided for [num], picks and displays a random quote

### !hello (anyone)
- Says hello back!

### !ping (anyone)
- Responds with Pong!

### !ads (VIPs/Mods only)
- Responds with a Github link with instructions on how to avoid ads on Twitch
- The link in question: [https://github.com/pixeltris/TwitchAdSolutions](https://github.com/pixeltris/TwitchAdSolutions)

### !help
- Responds with the list of commands and their usages
