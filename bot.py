import logging

from create_bot import dp, bot,con
from aiogram.utils import executor
#from aiogram.utils.executor import start_webhook

from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user


WEBHOOK_HOST = 'https://63-250-60-45.cloud-xip.com'
WEBHOOK_PATH = '/Bot3'
#WEBHOOK_PATH = '/path/to/api'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 443


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_echo(dp)


async def on_startup(_):
    #WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
    # 63-250-60-45.cloud-xip.com
#    await bot.set_webhook('https://63-250-60-45.cloud-xip.com/Bot3')
#    await bot.set_webhook('https://63.250.60.45:8443/Bot3')
    await bot.set_webhook(WEBHOOK_URL)
    con.message("Соединение с базой данных ...")
    print('Bot вышел в online ...')


async def on_shutdown(_):
    await bot.delete_webhook()
    print('Закрытие соединение ...')
    con.close()  # stop
    print('Bot закончил работу ...')


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)
logger.info("Start Bot ...  (запуск)")

register_all_filters(dp)  # Если Admin, то этот будет работат
register_all_handlers(dp)

if __name__ == '__main__':
#    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
#    Запускается  но нереагирует
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        )
