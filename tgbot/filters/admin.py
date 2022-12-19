import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config
from create_bot import con


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False
        config: Config = obj.bot.get('config')
        admins_tab = await con.admins()

#        print(admins_tab)

        return ((obj.from_user.id in config.tg_bot.admin_ids) or (obj.from_user.id in admins_tab)) == self.is_admin

