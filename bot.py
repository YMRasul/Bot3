from create_bot import dp, con,logger
from aiogram.utils import executor

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
#    con.message("Соединение с базой данных ...")
    print(">>>>>>> Start Bot oylik")
    logger.info(">>>>>>> Start Bot oylik")
    logger.info(">>>>>>> Connecting dbase_sqlite.db")
    logger.info('>>>>>>> Bot oylik in online')

async def on_shutdown(_):
    logger.info('>>>>>>> Close dbase_sqlite.db')
    con.close()  # stop
    logger.info('>>>>>>> Stop Bot oylik')
    print('>>>>>>> Stop Bot oylik')

register_all_filters(dp)  # Если Admin, то этот будет работат
register_all_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)

