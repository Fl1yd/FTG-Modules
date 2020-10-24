import requests
from .. import loader, utils


def register(cb):
    cb(WeatherMod())
    
class WeatherMod(loader.Module):
    """Погода с сайта wttr.in"""
    strings = {'name': 'Weather'}
    
    async def pwcmd(self, message):
        """"Кидает погоду картинкой.\nИспользование: .pw <город>."""
        args = utils.get_args_raw(message)
        city = args.replace(' ', '+')
        if not args:
            return await message.edit("Ты не указал город.")
        await message.edit("Узнаем погоду...")
        if args:
            city = f"https://wttr.in/{city}.png"
        await message.client.send_file(message.to_id, city)
        await message.delete()


    async def awcmd(self, message):
        """Кидает погоду ascii-артом.\nИспользование: .aw <город>."""
        city = utils.get_args_raw(message)
        if not city:
            return await message.edit("Ты не указал город.")
        await message.edit("Узнаем погоду...")
        if city:
            r = requests.get(f"https://wttr.in/{city}?0?q?T")
        await message.edit(f"<code>Город: {r.text}</code>")