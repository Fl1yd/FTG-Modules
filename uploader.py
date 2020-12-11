from .. import loader, utils


def register(cb):
    cb(UploaderMod())

class UploaderMod(loader.Module):
    """Загрузчик на fl1yd.ml"""
    strings = {'name': 'Uploader'}

    async def mulcmd(self, message):
        """Загрузить модуль на сервер."""
        name = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        fname = f'{name or reply.file.name}'
        await message.client.download_media(reply, f'/var/www/html/modules/{fname}')
        await message.edit(f'Модуль был сохранён как: <code>{fname}</code>.\n\n'
                           f'Вы можете его загрузить:  <code>.dlmod https://fl1yd.ml/modules/{fname}</code>')


    async def fulcmd(self, message):
        """Загрузить файл на сервер."""
        name = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        ext = reply.file.ext 
        fname = f'{name or message.id+reply.id}{ext}'
        await message.client.download_media(reply, f'/var/www/html/files/{fname}')
        await message.edit(f'Сохранено как: <code>https://fl1yd.ml/files/{fname}</code>')