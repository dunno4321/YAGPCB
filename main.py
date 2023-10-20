from server import end_server
from bot import Bot
import logging

bot = None
with open("assets/log.log", "w") as file:
    file.write("")
logging.basicConfig(filename="assets/log.log", level=logging.DEBUG)
logging.info("Hello world!")


try:
    bot = Bot("assets/client_config.json")
    logging.info("Starting Flask thread...")
    bot.run()
except KeyboardInterrupt:
    if bot is not None:
        bot.close()
    end_server()
