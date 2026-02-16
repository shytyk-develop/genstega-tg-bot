import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set")