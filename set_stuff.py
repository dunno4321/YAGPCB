import json

config = {
    "client_id": "",
    "client_secret": "",
    "channel": ""
}

print("This is where you will input data like Client ID and Client Secret")
print("This is used to authenticate the bot and enable it to send messages in chat")
print("All data is stored locally, in the config.json file")

config["client_id"] = input("Client ID: ")
config["client_secret"] = input("Client secret: ")
config["channel"] = input("Your channel name: ")

with open("config.json", "w") as file:
    json.dump(config, file)
print("Done! You should be able to run main.py with the command 'python main.py' now!")
