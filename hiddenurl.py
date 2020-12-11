import requests, io
from .. import loader, utils


def register(cb):
    cb(HiddenUrlMod())

class HiddenUrlMod(loader.Module):
    """Скрывает ссылку под невидимый текст."""
    strings = {'name': 'HiddenUrl'}

    async def hidecmd(self, message):
        """Используй .hide <url> <текст или реплай на медиа>."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if args or reply:
            await message.edit("Минуточку...")
            if reply:
                if reply.media:
                    file = io.BytesIO(await message.client.download_file(reply.media))
                    file.name = reply.file.name if reply.file.name else reply.file.id + reply.file.ext
                    try: x0at = requests.post('https://x0.at', files={'file': file})
                    except ConnectionError as e: return await message.edit(str(e))
                    await message.client.send_message(message.to_id, f'{args} <a href="{x0at.text}">\u2060</a>')
                else: return await message.edit("Это не реплай на медиа.")
            else:
                try: await message.client.send_message(message.to_id, f"{args.split(' ', 1)[1]} <a href=\"{args.split()[0]}\">\u2060</a>")
                except Exception as e: await message.client.send_message(message.to_id, f'<a href="{args}">\u2060</a>')
            await message.delete()
        else: return await message.edit("Нет аргументов или реплая на медиа.")