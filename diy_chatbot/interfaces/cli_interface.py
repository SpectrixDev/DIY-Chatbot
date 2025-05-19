from diy_chatbot.core.chatbot_engine import Chatbot
from pathlib import Path

def run_cli(db_path: str = None):
    """
    Run the chatbot in a command-line interface loop.
    """
    if db_path is None:
        db_path = str(Path(__file__).resolve().parent.parent.parent / "data" / "botBrain.sqlite")
    chatbot = Chatbot(db_path)
    print("DIY-Chatbot (CLI mode). Type Ctrl+C or Ctrl+D to exit.\n")
    bot_message = "Hello, world."
    try:
        while True:
            print(f"Bot: {bot_message}")
            user_input = input("You: ").strip()
            if not user_input:
                continue
            chatbot.learn(bot_message, user_input)
            bot_message = chatbot.get_response(user_input)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting chatbot. Goodbye!")
    finally:
        chatbot.close()
