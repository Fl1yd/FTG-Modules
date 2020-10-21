import os
from .. import loader, utils
from telethon import functions


def register(cb):
    cb(OnAvaMod())

class OnAvaMod(loader.Module):
    """Гифку/видео/стикер на аву."""
    strings = {'name': 'OnAva'}

    async def onavacmd(self, message):
        """Установить на аву гифку/видео/стикер.\nИспользование: .onava <реплай>."""
        try:
            await message.edit("Скачиваем...")
            reply = await message.get_reply_message()
            if reply:
                await message.edit("Конвертируем...")
                if reply.media.document.attributes:
                    if reply.video:
                        await message.client.download_media(reply.media, "ava.mp4")
                        os.system("ffmpeg -i ava.mp4 -c copy -an gifavaa.mp4 -y")
                        os.system("ffmpeg -i gifavaa.mp4 -vf scale=360:360 gifava.mp4 -y")
                    else:
                        await message.client.download_media(reply.media, "tgs.tgs")
                        os.system("lottie_convert.py tgs.tgs tgs.gif; mv tgs.gif gifava.mp4")
            else:
                return await message.edit("Нет реплая на гиф/анимированный стикер/видеосообщение.")
            await message.edit("Устанавливаем аву...")
            await message.client(functions.photos.UploadProfilePhotoRequest(video=await message.client.upload_file("gifava.mp4"), video_start_ts=0.0))
            await message.edit("Ава установлена.")
            try:
                os.remove("ava.mp4")
                os.remove("gifava.mp4")
                os.remove("gifavaa.mp4")
            except FileNotFoundError:
                pass
        except Exception as e:
            await message.client.send_message(message.to_id, str(e))
            await message.edit("Блин, какой я дурак, я не отличаю гифку/анимированный стикер/видео от любого другого файла.\n\n"
                               "<b>ЭТОТ ФАЙЛ НЕ ПОДДЕРЖИВАЕТСЯ!!!</b>(либо просто какая-то тех.ошибка c: )")
            try:
                os.remove("ava.mp4")
                os.remove("gifava.mp4")
                os.remove("gifavaa.mp4")
                os.remove("tgs.*")
            except FileNotFoundError:
                pass
            return


    async def togifcmd(self, message):
        """Сделать из медиа гифку.\nИспользование: .togif <реплай>."""
        try:
            await message.edit("Конвертируем...")
            reply = await message.get_reply_message()
            if reply:
                await message.client.download_media(reply.media, "tgs.tgs")
                os.system("lottie_convert.py tgs.tgs tgs.gif")
                await message.edit("Отправляем...")
                await message.client.send_file(message.to_id, "tgs.gif")
                await message.delete()
                try:
                    os.remove("tgs.*")
                except FileNotFoundError:
                    pass
            else:
                return await message.edit("Нет реплая на гиф/анимированный стикер/видеосообщение.")
        except:
            await message.edit("Блин, какой я дурак, я не отличаю гифку/анимированный стикер/видео от любого другого файла.\n\n"
                               "<b>ЭТОТ ФАЙЛ НЕ ПОДДЕРЖИВАЕТСЯ!!!</b>(либо просто какая-то тех.ошибка c: )")
            try:
                os.remove("tgs.*")
            except FileNotFoundError:
                pass
            return