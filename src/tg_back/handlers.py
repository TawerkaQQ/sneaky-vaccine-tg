from io import BytesIO
import os
import sys
from pymongo import MongoClient

from aiogram import F, Router, types, flags
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.types import InputFile

current_directory = os.path.dirname(__file__)
tg_front = os.path.join(current_directory, '..', 'tg_front')
sys.path.append(tg_front)
db = os.path.join(current_directory, '..', 'db')

from tg_front import keyboard_button as kb
from tg_front.text import TextTypes
from db.db_connector import users
from .states import PState


router = Router()

async def auth_check(msg: Message) -> bool:
    user = await users.find_one({'telegram_id': msg.from_user.id})
    return True if user else False

@router.message(Command("start"))
async def start_handler(msg: Message):
    user = await users.find_one({'telegram_id': msg.from_user.id})
    print(user)
    if user:
        await msg.answer(TextTypes.GREET.format(name=msg.from_user.full_name), reply_markup=kb.start_buttons)
    else:
        await msg.answer(TextTypes.UNSUCCESSFUL_AUTH, parse_mode='HTML')

@router.message(Command("auth"))
async def auth_handler(msg: Message, state: FSMContext):
    user = await users.find_one({'telegram_id': msg.from_user.id})
    if user:
        return
    
    input_message = msg.text.split(' ')
    if (len(input_message) == 1):
        await msg.answer(TextTypes.AUTH_INPUT_TOKEN)
        await state.set_state(PState.waiting_for_token)
    else:
        token = input_message[1]
        user_with_token = await user_has_token(token)
        if  (user_with_token is not None):
            await users.update_one(
                {"name": user_with_token["name"]},
                {"$set": {'telegram_id': msg.from_user.id}}
            )
            await msg.answer(TextTypes.AUTH_COMPLETE)
            await state.clear()
        else:
            await msg.answer(TextTypes.WRONG_TOKEN)
        return

@router.message(PState.waiting_for_token)
async def token_input(msg: Message, state: FSMContext):
    token = msg.text.strip()
    user_with_token = await user_has_token(token)
    if (user_with_token is not None):
        await users.update_one(
            {"name": user_with_token["name"]},
            {"$set": {'telegram_id': msg.from_user.id}}
        )
        await msg.answer(TextTypes.AUTH_COMPLETE)
        await state.clear()
    else:
        await msg.answer(TextTypes.WRONG_TOKEN)
    return


async def user_has_token(token: str):
    user_with_token = await users.find_one(
        {
            'tgTokens.token': token
        }
    )
    return user_with_token if user_with_token else None
