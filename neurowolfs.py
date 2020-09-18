from .. import loader
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError


def register(cb):
    cb(VsratoMod())

class VsratoMod(loader.Module):
    """Нейроволки"""
    strings = {'name': 'Нейроволк Акела'}

    async def wolfcmd(self, event):
        """"Используй .wolf, чтобы получить рандомную пикчу нейроволка."""
        chat = "@neuroakelabot"
        await event.edit("<b>Минуточку...</b>")
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=979556006))
                await event.client.send_message(chat, "Дай мне мем, Акела")
                response = await response
            except YouBlockedUserError:
                await event.edit("<b>Разблокируй @neuroakelabot.</b>")
                return
            await event.client.send_file(event.to_id, response.media)
        await event.delete()