import asyncio
from .. import loader
from telethon import events
from datetime import datetime
from telethon.tl.types import User, Chat, Channel


def register(cb):
    cb(CountMod())

class CountMod(loader.Module):
    """Количество чатов."""
    strings = {'name': 'Count'}

    async def countcmd(self, message):
        if message.fwd_from:
            return
        start = datetime.now()
        users = 0
        groups = 0
        supergroups = 0
        channels = 0
        bots = 0
        await message.edit("<b>Получаем информацию...</b>")
        async for dlgs in message.client.iter_dialogs(limit=None):
            if dlgs.is_user:
                if dlgs.entity.bot:
                    bots += 1
                else:
                    users += 1
            elif dlgs.is_channel:
                if dlgs.entity.broadcast:
                    channels += 1
                else:
                    supergroups += 1
            elif dlgs.is_group:
                groups += 1
        end = datetime.now()
        ms = ((end - start)//1000).microseconds
        await message.edit(f"<b>Подсчитано за</b> <code>{ms}</code> <b>мс.</b>\n"
                           f"<b>Количество моих чатов в Telegram:</b>\n"
                           f"<b>Пользователей:</b> <code>{users}</code>\n"
                           f"<b>Групп:</b> <code>{groups}</code>\n"
                           f"<b>Супер Групп:</b> <code>{supergroups}</code>\n"
                           f"<b>Каналов:</b> <code>{channels}</code>\n"
                           f"<b>Ботов:</b> <code>{bots}</code>")
