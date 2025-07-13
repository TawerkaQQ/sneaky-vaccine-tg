import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.chat_action import ChatActionMiddleware

current_directory = os.path.dirname(__file__)
tg_back = os.path.join(current_directory, '..', 'tg_back')
sys.path.append(tg_back)

from tg_back.handlers import router

load_dotenv()
TOKEN = os.getenv('TG_API_TOKEN')

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())