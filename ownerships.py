from .. import loader
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest


def register(cb):
    cb(OwnershipsMod())
    
class OwnershipsMod(loader.Module):
    """Посмотреть свои владения."""
    strings = {'name': 'Ownerships'}
    
    async def owncmd(self, message):
        """Команда .own выводит список владений открытых чатов/каналов. """
        await message.edit('<b>Считаем...</b>')
        result = await message.client(GetAdminedPublicChannelsRequest())
        msg = ""
        count = 0
        for obj in result.chats:
            count += 1
            msg += f'\n• <a href="tg://resolve?domain={obj.username}">{obj.title}</a> <b>|</b> <code>{obj.id}</code>'
        await message.edit(f'<b>Мои владения: {count}</b>\n {msg}')