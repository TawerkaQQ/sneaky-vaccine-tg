from aiogram.fsm.state import StatesGroup, State

class PState(StatesGroup):
    waiting_for_token = State()
    load_image = State()
    waiting_for_auth = State()