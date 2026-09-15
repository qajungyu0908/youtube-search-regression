"""Post a Jenkins build summary to Telegram using injected Jenkins credentials."""

import os

import requests


def main() -> None:
    response = requests.post(
        f"https://api.telegram.org/bot{os.environ['TG_BOT_TOKEN']}/sendMessage",
        data={
            "chat_id": os.environ["TG_CHAT_ID"],
            "text": os.environ["TELEGRAM_MESSAGE"],
        },
        timeout=15,
    )
    response.raise_for_status()


if __name__ == "__main__":
    main()
