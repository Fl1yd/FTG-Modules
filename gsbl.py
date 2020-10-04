import io
from .. import loader 
from PIL import Image
from gsbl.stick_bug import StickBug


def register(cb):
    cb(GSBLMod()) 

class GSBLMod(loader.Module):
    """Фановый, мемный модуль."""
    strings = {'name': 'Get-Stick-Bugged-Lol'} 
    
    async def gsblcmd(self, event):
        """Используй .gsbl <реплай на видео>."""
        reply = await event.get_reply_message() 
        if not reply:
            await event.edit("Нет реплая на видео.")
            return 
        await event.edit("Минуточку...")
        im = io.BytesIO()
        await event.edit("Скачиваю...")
        await event.client.download_file(reply, im)
        await event.edit("Обрабатываю...") 
        im = Image.open(im)
        sb = StickBug(im)
        video = sb.video
        sb.save_video("get_stick_bugged_lol.mp4")
        await event.edit("Отправляю...")
        await event.client.send_file(event.to_id, open("get_stick_bugged_lol.mp4", "rb"), reply_to=reply)
        await message.delete()