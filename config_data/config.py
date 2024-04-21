from dataclasses import dataclass

from config_data.env import BOT_TOKEN, ADMIN_IDS


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    return Config(tg_bot=TgBot(
        token=BOT_TOKEN,
        admin_ids=list(map(int, ADMIN_IDS))))
