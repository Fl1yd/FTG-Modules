from .. import loader
from telethon.tl.functions.channels import LeaveChannelRequest
from userbot import bot

def register(cb):
    cb(ChatMod())

class ChatMod(loader.Module):
    """Чат модуль"""
    strings = {'name': 'Chat'}

    async def useridcmd(self, usrid):
        """Команда .userid показывает ID выбранного пользователя"""
        message = await usrid.get_reply_message()
        if message:
            if not message.forward:
                user_id = message.sender.id
                if message.sender.username:
                    name = "@" + message.sender.username
                else:
                    name = "**" + message.sender.first_name + "**"

            else:
                user_id = message.forward.sender.id
                if message.forward.sender.username:
                    name = "@" + message.forward.sender.username
                else:
                    name = "*" + message.forward.sender.first_name + "*"
            await usrid.edit("<b>Имя:</b> {} \n<b>ID:</b> <code>{}</code>".format(name, user_id))


    async def chatidcmd(self, chtid):
        """Команда .chatid показывает ID чата."""
        await chtid.edit("<b>Чат ID:</b>\n<code>" + str(chtid.chat_id) + "</code>")


    async def kickmecmd(self, leave):
        """Используйте команду .kickme, чтобы кикнуть себя из чата."""
        await leave.edit("<b>До связи.</b>")
        await bot(LeaveChannelRequest(leave.chat_id))