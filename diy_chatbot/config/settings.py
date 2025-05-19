import os
import json
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DEFAULT_DB_PATH = DATA_DIR / "botBrain.sqlite"
CONFIG_FILE_PATH = BASE_DIR / "config.json"

def load_config():
    if CONFIG_FILE_PATH.exists():
        with open(CONFIG_FILE_PATH, "r") as f:
            return json.load(f)
    return {}

config_data = load_config()

DATABASE_PATH = os.environ.get("DATABASE_PATH") or str(config_data.get("database_path", DEFAULT_DB_PATH))
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN") or config_data.get("discordBotToken")
CHATBOT_CHANNEL_ID = os.environ.get("CHATBOT_CHANNEL_ID") or config_data.get("chatbotChannelID")
