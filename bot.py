import logging

from create_bot import dp, bot,con
from aiogram.utils import executor
#from aiogram.utils.executor import start_webhook

from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_echo(dp)


async def on_startup(_):
    await bot.set_webhook('https://63.250.60.45:80/root/Bot3')
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
    executor.start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=5000
        )
