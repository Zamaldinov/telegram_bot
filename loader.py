import os
import logging
from aiogram import Bot, Dispatcher
from api import Controller
from aiogram.fsm.storage.memory import MemoryStorage
from db import DB_Controller
from handlers.utils import SlowpokeMiddleware
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
# Объект бота
# доставать настройки из .env
load_dotenv()
token = os.getenv('BOT_TOKEN')
bot = Bot(token=token)
# Диспетчер
dp = Dispatcher(storage=MemoryStorage())

api_controller = Controller()
db_control = DB_Controller()
db_control.create_all_tables()

command_middleware = SlowpokeMiddleware(db_control)
dp.message.middleware.register(command_middleware)

# delete_middleware = CallbackDeleteMiddleware()
# dp.callback_query.middleware.register(delete_middleware)