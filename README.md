# 🗣 DIY-Chatbot

DIY-Chatbot is a Python chatbot I made back in 2018 that learns from conversations by associating user replies with previous bot messages. It uses a simple association-based algorithm and stores its knowledge in an SQLite database. The bot can be run in the terminal or as a Discord bot.

---

## How It Works: Example Flow

1. The bot starts with no knowledge.
2. You say something to the bot:
   ```
   Bot: Hello
   User: Hi there!
   ```
3. The bot stores "Hi there!" as a possible reply to "Hello".
4. Next time anyone says "Hello", the bot may reply "Hi there!" based on its learned associations.

---

## Setup Guide

### Requirements

- Python 3.8+
- SQLite (bundled with Python)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/DIY-Chatbot.git
   cd DIY-Chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

For the Discord bot, copy `config.json.example` to `config.json` and fill in your credentials:
```json
{
  "discordBotToken": "YOUR_DISCORD_BOT_TOKEN",
  "chatbotChannelID": 123456789012345678
}
```

---

## Usage

### Command-Line Interface

Start a chat session in your terminal:
```bash
python run.py cli
```

- The bot uses `data/botBrain.sqlite` by default.
- To use a pre-made model, copy it to `data/botBrain.sqlite` or specify with `--db-path`.

### Discord Bot

1. Set up your Discord bot and get your bot token and channel ID.
2. Configure your credentials as described above.
3. Run the Discord bot:
   ```bash
   python run.py discord
   ```

---

## Pre-Made Models

- Pre-trained brains are in `data/pre_made_models/`.
- To use one, copy it to `data/botBrain.sqlite` or specify its path with `--db-path`.

---

## License

MIT License.
