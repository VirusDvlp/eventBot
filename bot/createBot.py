from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, HOST, DB_USER, DB_NAME, PORT, PASSWORD, ADMIN_ID
from database import DataBase


storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

db = DataBase(
    host=HOST,
    user=DB_USER,
    password=PASSWORD,
    database=DB_NAME,
    port=PORT
)
