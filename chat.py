from .. import loader, utils
from os import remove
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.errors.rpcerrorlist import MessageTooLongError
from telethon.errors import ChatAdminRequiredError
from telethon.tl.types import ChannelParticipantsAdmins
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


    async def userscmd(self, message):
        """Команда .users выводит список всех пользователей в чате."""
        info = await message.client.get_entity(message.chat_id)
        title = info.title if info.title else "this chat"
        mentions = '<b>Пользователей в {}:</b> \n'.format(title)
        try:
            if not utils.get_args_raw(message):
                async for user in message.client.iter_participants(message.chat_id):
                    if not user.deleted:
                        mentions += (f"\n<a href =\"tg://user?id={user.id}\">{user.first_name}</a> <code>{user.id}</code>")
                    else:
                        mentions += f"\nУдалённый аккаунт<code>{user.id}</code>"
            else:
                searchq = utils.get_args_raw(message)
                async for user in message.client.iter_participants(
                        message.chat_id, search=f'{searchq}'):
                    if not user.deleted:
                        mentions += (f"\n<a href =\"tg://user?id={user.id}\">{user.first_name}</a> <code>{user.id}</code>")
                    else:
                        mentions += f"\nУдалённый аккаунт <code>{user.id}</code>"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        try:
            await message.edit(mentions)
        except MessageTooLongError:
            await message.edit('<b>Черт, слишком большой чат. Загружаю список пользователей в файл...</b>')
            file = open("userslist.md", "w+")
            file.write(mentions)
            file.close()
            await message.client.send_file(
                message.chat_id,
                "userslist.md",
                caption='Пользователей в {}'.format(title),
                reply_to=message.id,
            )
            remove("userslist.md")


    async def adminscmd(self, message):
        """Команда .admins показывает список всех админов в чате."""
        info = await message.client.get_entity(message.chat_id)
        title = info.title if info.title else "this chat"
        mentions = f'<b>Админов в {title}:</b> \n'
        try:
            async for user in message.client.iter_participants(
                    message.chat_id, filter=ChannelParticipantsAdmins):
                if not user.deleted:
                    link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                    userid = f"<code>{user.id}</code>"
                    mentions += f"\n{link} {userid}"
                else:
                    mentions += f"\nУдалённый аккаунт <code>{user.id}</code>"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        try:
            await message.edit(mentions, parse_mode="html")
        except MessageTooLongError:
            await message.edit(
                "Черт, слишком много админов здесь. Загружаю список админов в файл...")
            file = open("adminlist.txt", "w+")
            file.write(mentions)
            file.close()
            await message.client.send_file(message.chat_id,
                                           "adminlist.txt",
                                           caption='Админов в {}'.format(title),
                                           reply_to=message.id)
            remove("adminlist.txt")