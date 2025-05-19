import argparse
from diy_chatbot.config import settings
from diy_chatbot.interfaces import cli_interface, discord_interface

def main():
    parser = argparse.ArgumentParser(description="DIY-Chatbot: Modular Chatbot Application")
    parser.add_argument(
        "interface",
        choices=["cli", "discord"],
        help="Choose which interface to run: 'cli' for command-line, 'discord' for Discord bot."
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default=settings.DATABASE_PATH,
        help="Path to the SQLite database file."
    )
    parser.add_argument(
        "--discord-token",
        type=str,
        default=settings.DISCORD_BOT_TOKEN,
        help="Discord bot token (overrides config/env)."
    )
    parser.add_argument(
        "--channel-id",
        type=int,
        default=settings.CHATBOT_CHANNEL_ID,
        help="Discord channel ID for the bot (overrides config/env)."
    )
    args = parser.parse_args()

    if args.interface == "cli":
        cli_interface.run_cli(db_path=args.db_path)
    elif args.interface == "discord":
        discord_interface.run_discord(
            db_path=args.db_path,
            discord_token=args.discord_token,
            chatbot_channel_id=args.channel_id
        )

if __name__ == "__main__":
    main()
