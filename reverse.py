from .. import loader, utils


def register(cb):
    cb(ReverseMod())
    
class ReverseMod(loader.Module):
    """Реверс текста."""
    strings = {'name': 'Reverse'}

    async def revcmd(self, message):
        """Используй .rev <текст или реплай>."""
        text = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not text and not reply:
            return await message.edit("Нет текста или реплая.")
        if reply:
            return await message.edit(f"{reply.raw_text}"[::-1])
        if text:
            return await message.edit(f"{text}"[::-1])