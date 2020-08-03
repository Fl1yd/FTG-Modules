from telethon import events
from .. import loader, utils
import calendar


def register(cb):
    cb(CalendarMod())


class CalendarMod(loader.Module):
    """Календарь"""
    strings = {"name": "Calendar"}

    async def clndcmd(self, event):
        """.clnd <год> <месяц>"""
        args = utils.get_args(event)
        year = int(args[0]) if args else None
        month = int(args[1]) if len(args) == 2 else None

        if not year:
            await event.edit('<b>Ты не написал год... 😔</b>')
        if not month:
            await event.edit('<b>Ты не написал месяц... 😔</b>')

        await event.edit(f"<code>{calendar.month(year, month)}</code>")