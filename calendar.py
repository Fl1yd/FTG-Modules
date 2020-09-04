from .. import loader, utils
import calendar
from datetime import date


def register(cb):
    cb(CalendarMod())

class CalendarMod(loader.Module):
    """Календарь"""
    strings = {"name": "Calendar"}

    async def clndcmd(self, event):
        """.clnd <год> <месяц> или ничего"""
        args = utils.get_args(event)
        y, m, d = [int(i) for i in str(date.today()).split("-")]
        year = int(args[0]) if args and args[0].isdigit() else y
        month = int(args[1]) if len(args) == 2 and args[1].isdigit() and int(args[1]) in range(1, 13) else m
        calen = calendar.month(year, month)
        if year == y and month == m:
            calen = calen.replace(str(d), f'</code><strong>{d}</strong><code>')
        await event.edit(f"<code>\u2060{calen}</code>")