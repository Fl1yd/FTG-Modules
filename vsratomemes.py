from .. import loader, utils
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import io
from io import BytesIO
from PIL import Image


def register(cb):
    cb(VsratoMemesMod())

class VsratoMemesMod(loader.Module):
    """Всратые мемы."""
    strings = {'name': 'Всратые мемы'}

    async def wolfcmd(self, event):
        """"Используй .wolf."""
        chat = "@neuroakelabot"
        await event.edit("<b>Минуточку...</b>")
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=979556006))
                await event.client.send_message(chat, "Дай мне мем, Акела")
                response = await response
            except YouBlockedUserError:
                await event.edit("<b>Разблокируй @neuroakelabot</b>")
                return
            await event.client.send_file(event.to_id, response.media)
        await event.delete()


    async def vsratocmd(self, event):
        """Используй .vsrato <реплай на пикчу>."""
        reply = await event.get_reply_message()
        if not reply:
            await event.edit("<b>Нет реплая на пикчу.</b>")
            return
        else:
            pic = await check_media(event, reply)
            if not pic:
                await utils.answer(event, "<b>Это не изображение.</b>")
                return
        chat = '@vsratoslavbot'
        await event.edit("<b>Минуточку...</b>")
        async with event.client.conversation(chat) as conv:
            try:
                medias = kekw(pic)
                await event.client.send_file(chat, medias)
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=1066090937))
                response = await response
                if response.media:
                    lol = await response.media
                else:
                    response = conv.wait_event(events.NewMessage(incoming=True, from_users=1066090937))
                    response = await response
            except YouBlockedUserError:
                await event.reply("<b>Разблокируй @vsratoslavbot.</b>")
                return
            await event.client.send_file(event.to_id, response.media, reply_to=await event.get_reply_message())
        event.delete()


async def check_media(message, reply):
    if reply and reply.media:
        if reply.photo:
            data = reply.photo
        elif reply.document:
            if reply.gif or reply.video or reply.audio or reply.voice:
                return None
            data = reply.media.document
        else:
            return None
    else:
        return None
    if not data or data is None:
        return None
    else:
        data = await message.client.download_file(data, bytes)
        try:
            Image.open(io.BytesIO(data))
            return data
        except:
            return None

def kekw(reply):
    scrrrra = Image.open(BytesIO(reply))
    out = io.BytesIO()
    out.name = "outsider.png"
    scrrrra.save(out)
    return out.getvalue()
