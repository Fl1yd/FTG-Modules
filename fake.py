from random import choice, randint
from .. import loader, utils
from asyncio import sleep


def register(cb):
    cb(FakeMod()) 
    
class FakeMod(loader.Module):
    """Показывает фейковые действия."""
    strings = {'name': 'Fake Actions'} 
    
    async def fakecmd(self, event):
        """Использование: .fake <действие>.\nСписок действий: typing, contact, game, location, voice, round, video, photo, document.\nОтмена: .fake cancel"""
        options = ['typing', 'contact', 'game', 'location', 'voice', 'round', 'video','photo', 'document', 'cancel']
        input_str = utils.get_args_raw(event)
        args = input_str.split()
        if len(args) == 0:
            scam_action = choice(options)
            scam_time = randint(30, 60)
        elif len(args) == 1:
            try:
                scam_action = str(args[0]).lower()
                scam_time = randint(30, 60)
            except ValueError:
                scam_action = choice(options)
                scam_time = int(args[0])
        elif len(args) == 2:
            scam_action = str(args[0]).lower()
            scam_time = int(args[1])
        else:
            await event.edit('<b>Неправильный ввод.</b>')
            return
        try:
            if (scam_time > 0):
                await event.delete()
                async with event.client.action(event.chat_id, scam_action):
                    await sleep(scam_time)
        except BaseException:
            return