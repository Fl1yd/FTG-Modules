from .. import loader, utils
import logging
from telethon import functions, types

logger = logging.getLogger(__name__)

def register(cb):
	cb(ReportMod())
	
class ReportMod(loader.Module):
    """Репорт"""
    strings = {"name": "Report",
               "who_to_report": "<b>Кого я должен зарепортить?</b>",
               "reported": "<b>Ты получил репорт за спам!</b>"} 

    async def client_ready(self, client, db):
        self._db = db

    async def reportcmd(self, message):
        """Репорт пользователя за спам."""
        user = await utils.get_target(message)
        if not user:
            await utils.answer(message, self.strings("who_to_report", message))
            return
        self._db.set(__name__, "allow", list(set(self._db.get(__name__, "allow", [])).difference({user})))
        if message.is_reply and isinstance(message.to_id, types.PeerChannel):
            await message.client(functions.messages.ReportRequest(peer=message.chat_id,
                                                                  id=[message.reply_to_msg_id],
                                                                  reason=types.InputReportReasonSpam()))
        else:
            await message.client(functions.messages.ReportSpamRequest(peer=message.to_id))
        await utils.answer(message, self.strings("reported", message))