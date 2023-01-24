import logging
from aiogram import Bot, Dispatcher
from tgbot.config import load_config,Config
from tgbot.sqldb import Database
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import date


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,filename='oylikbot.log',
    format=u'%(levelname)-8s [%(asctime)s] %(message)s'
)
'''
logging.basicConfig(
    level=logging.INFO,filename='oylikbot.log',
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
)
'''
today = date.today()

config = load_config(".env")
#config = load_config()


storage = MemoryStorage()

con = Database('dbase_sqlite.db')
bot = Bot(token=config.tg_bot.token,parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)


superuser = config.tg_bot.superuser

bot['config'] = config

