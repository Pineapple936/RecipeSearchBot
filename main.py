from bot.server import *
from os import getenv
from dotenv import load_dotenv

def main() -> None:
    load_dotenv()
    bot = Bot(getenv("API_KEY"))
    bot.run()

if __name__ == "__main__":
    main()
