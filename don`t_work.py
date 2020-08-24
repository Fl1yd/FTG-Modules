from .. import loader


def register(cb):
    cb(DontWorkMod())

class DontWorkMod(loader.Module):
    """Модуль не работает."""
    strings = {'name': 'Don`t Work'}

    async def dontworkcmd(self, message):
        """Используй .dontwork, чтобы понять, что модуль не работает."""
        dontwork = '<b>Модуль не работает.</b>'
        await message.edit(dontwork)