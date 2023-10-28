import json

config = {
    "client_id": "",
    "client_secret": "",
    "channel": ""
}

print("This is where you will input data like Client ID and Client Secret")
print("This is used to authenticate the bot and enable it to send messages in chat")
print("All data is stored locally, in the config.json file")

config["client_id"] = input("Client ID: ").strip()
config["client_secret"] = input("Client secret: ").strip()
config["channel"] = input("Your channel name: ").strip()

with open("assets/config.json", "w") as file:
    json.dump(config, file)

print("Done! You should be able to run main.py with the command 'python main.py' now!")
