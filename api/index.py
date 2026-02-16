import os
import logging
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.handlers import router

# Setup
BOT_TOKEN = os.environ.get("BOT_TOKEN")
app = FastAPI()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

@app.post("/api/webhook")
async def webhook_handler(request: Request):
    """Handle Telegram webhook updates"""
    try:
        update_data = await request.json()
        update = types.Update(**update_data)
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Error in webhook: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def index():
    return {"status": "Bot is running on Vercel!"}