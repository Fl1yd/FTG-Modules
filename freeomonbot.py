from .. import loader, utils
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError


def register(cb):
    cb(OmonBotMod())

class OmonBotMod(loader.Module):
    """Омон бот."""
    strings = {'name': 'FreeOmonBot'}

    async def omoncmd(self, message):
        """Используй .omon <реплай на пикчу>."""
        chat = "@FreeOmonBot"
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("<b>Нет реплая.</b>")
            return
        await message.edit("<b>Минуточку...</b>")
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=775654752))
                await message.client.send_message(chat, reply)
                response = await response
            except YouBlockedUserError:
                await message.edit("<b>Разблокируй @FreeOmonBot</b>")
                return
        if response.text:
            pass
        if response.media:
            await message.client.send_file(message.to_id, response.media)
            await message.delete()