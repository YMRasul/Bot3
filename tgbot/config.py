from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    admin_ids: list
    superuser: int


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str = None):
    #    print("sdrfsdfsdgdfgds",path)
    env = Env()
    #    print(env)
    env.read_env(path)
    conf = Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            superuser=env.int("SUPERUSER"),
        )
    )
    return conf
