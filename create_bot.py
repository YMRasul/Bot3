from aiogram import Bot, Dispatcher
from tgbot.config import load_config
from tgbot.sqldb import Database
from aiogram.contrib.fsm_storage.memory import MemoryStorage

config = load_config(".env")
#config = load_config()

storage = MemoryStorage()

con = Database('dbase_sqlite.db')
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

bot['config'] = config
