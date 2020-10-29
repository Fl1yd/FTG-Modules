import requests
from .. import loader, utils


def register(cb):
    cb(WeatherMod())
    
class WeatherMod(loader.Module):
    """Погода с сайта wttr.in"""
    strings = {'name': 'Weather'}
    
    async def pwcmd(self, message):
        """"Кидает погоду картинкой.\nИспользование: .pw <город>; ничего."""
        args = utils.get_args_raw(message)
        city = args.replace(' ', '+')
        city = f"https://wttr.in/{city if city != None else ''}.png"
        await message.client.send_file(message.to_id, city)
        await message.delete()


    async def awcmd(self, message):
        """Кидает погоду ascii-артом.\nИспользование: .aw <город>; ничего."""
        city = utils.get_args_raw(message)
        await message.edit("Узнаем погоду...")
        r = requests.get(f"https://wttr.in/{city if city != None else ''}?0?q?T&lang=ru")
        await message.edit(f"<code>Город: {r.text}</code>")