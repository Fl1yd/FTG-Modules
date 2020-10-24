from .. import loader, utils
from telethon import functions


def register(cb):
    cb(ReportMod())

class ReportMod(loader.Module):
    """Репорт"""
    strings = {"name": "Report"}

    async def reportcmd(self, message):
        """Репорт пользователя за спам."""
        reply = await message.get_reply_message()
        if reply:
            await message.client(functions.messages.ReportSpamRequest(peer=reply.sender.id))
            await message.edit("<b>Ты получил репорт за спам!</b>")
        else:
            return await message.edit("<b>Кого я должен зарепортить?</b>")