# Chat Module for Friendly-Telegram UserBot.
# Copyright (C) 2020 @Fl1yd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ======================================================================

import logging
from .. import loader, utils
from os import remove
from telethon.tl.functions.channels import LeaveChannelRequest, InviteToChannelRequest 
from telethon.errors import (UserIdInvalidError, UserNotMutualContactError, UserPrivacyRestrictedError, BotGroupsBlockedError, ChannelPrivateError, YouBlockedUserError,  MessageTooLongError,
                             UserBlockedError, ChatAdminRequiredError, UserKickedError, InputUserDeactivatedError, ChatWriteForbiddenError, UserAlreadyParticipantError)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (ChannelParticipantsAdmins, PeerChat, ChannelParticipantsBots)
from telethon.tl.functions.messages import AddChatUserRequest
def register(cb):
    cb(ChatMod())

class ChatMod(loader.Module):
    """Чат модуль"""
    strings = {'name': 'ChatModule'}

    async def useridcmd(self, message):
        """Команда .userid <@ или реплай> показывает ID выбранного пользователя."""
        if message.is_reply:
            full = await message.client(GetFullUserRequest((await message.get_reply_message()).from_id))
        else:
            args = utils.get_args(message)
            try:
                full = await message.client(GetFullUserRequest(args[0]))
            except:
                full = await message.client(GetFullUserRequest(message.from_id))
        info = (f"<b>Имя:</b> <code>{full.user.first_name}</code>\n"
                f"<b>ID:</b> <code>{full.user.id}</code>")
        await message.edit(info)


    async def chatidcmd(self, message):
        """Команда .chatid показывает ID чата."""
        args = utils.get_args_raw(message)
        chatid = None
        if args:
            if args.isnumeric(): args = int(args)
            try: chatid = await message.client.get_entity(args)
            except: chatid = await message.client.get_entity(message.to_id)
        else: chatid = await message.client.get_entity(message.to_id)
        await message.edit(f"<b>Название:</b> <code>{chatid.title}</code>\n"
                           f"<b>ID</b>: <code>{chatid.id}</code>")


    async def invitecmd(self, event):
        """Используйте .invite <@ или реплай>, чтобы добавить пользователя в чат."""
        if event.fwd_from:
            return
        to_add_users = utils.get_args_raw(event)
        reply = await event.get_reply_message()
        if not to_add_users and not reply:
            await event.edit("<b>Нет аргументов.</b>")
        elif reply:
            to_add_users = str(reply.from_id)
        if to_add_users:
            if not event.is_group and not event.is_channel:
                return await event.edit("<b>Это не чат!</b>")
            else:
                if not event.is_channel and event.is_group:
                    # https://tl.telethon.dev/methods/messages/add_chat_user.html
                    for user_id in to_add_users.split(" "):
                        try:
                            userID = int(user_id)
                        except:
                            userID = user_id

                        try:
                            await event.client(AddChatUserRequest(chat_id=event.chat_id,
                                                                  user_id=userID,
                                                                  fwd_limit=1000000))
                        except ValueError:
                            return await event.reply("<b>Неверный @ или ID.</b>")
                        except UserIdInvalidError:
                            return await event.reply("<b>Неверный @ или ID.</b>")
                        except UserPrivacyRestrictedError:
                            return await event.reply("<b>Настройки приватности пользователя не позволяют пригласить его.</b>")
                        except UserNotMutualContactError:
                            return await event.reply("<b>Настройки приватности пользователя не позволяют пригласить его.</b>")
                        except ChatAdminRequiredError:
                            return await event.reply("<b>У меня нет прав.</b>")
                        except ChatWriteForbiddenError:
                            return await event.reply("<b>У меня нет прав.</b>")
                        except ChannelPrivateError:
                            return await event.reply("<b>У меня нет прав.</b>")
                        except UserKickedError:
                            return await event.reply("<b>Пользователь кикнут из чата, обратитесь к администраторам.</b>")
                        except BotGroupsBlockedError:
                            return await event.reply("<b>Бот заблокирован в чате, обратитесь к администраторам.</b>")
                        except UserBlockedError:
                            return await event.reply("<b>Пользователь заблокирован в чате, обратитесь к администраторам.</b>")
                        except InputUserDeactivatedError:
                            return await event.reply("<b>Аккаунт пользователя удалён.</b>")
                        except UserAlreadyParticipantError:
                            return await event.reply("<b>Пользователь уже в группе.</b>")
                        except YouBlockedUserError:
                            return await event.reply("<b>Вы заблокировали этого пользователя.</b>")
                    await event.edit("<b>Пользователь приглашён успешно!</b>")
                else:
                    # https://tl.telethon.dev/methods/channels/invite_to_channel.html
                    for user_id in to_add_users.split(" "):
                        try: userID = int(user_id)
                        except: userID = user_id
                        try:
                            await event.client(InviteToChannelRequest(channel=event.chat_id,
                                                                                         users=[userID]))
                        except ValueError:
                            return await event.reply("<b>Неверный @ или ID.</b>")
                        except UserIdInvalidError:
                            return await event.reply("<b>Неверный @ или ID.</b>")
                        except UserPrivacyRestrictedError:
                            return await event.reply("<b>Настройки приватности пользователя не позволяют пригласить его.</b>")
                        except UserNotMutualContactError:
                            return await event.reply("<b>Настройки приватности пользователя не позволяют пригласить его.</b>")
                        except ChatAdminRequiredError:
                            return await event.reply("<b>У меня нет прав.</b>")
                        except ChatWriteForbiddenError:
                            return await event.reply("<b>У меня нет прав.</b>")
                        except ChannelPrivateError:
                            return await event.reply("<b>У меня нет прав.</b>")
                        except UserKickedError:
                            return await event.reply("<b>Пользователь кикнут из чата, обратитесь к администраторам.</b>")
                        except BotGroupsBlockedError:
                            return await event.reply("<b>Бот заблокирован в чате, обратитесь к администраторам.</b>")
                        except UserBlockedError:
                            return await event.reply("<b>Пользователь заблокирован в чате, обратитесь к администраторам.</b>")
                        except InputUserDeactivatedError:
                            return await event.reply("<b>Аккаунт пользователя удалён.</b>")
                        except UserAlreadyParticipantError:
                            return await event.reply("<b>Пользователь уже в группе.</b>")
                        except YouBlockedUserError:
                            return await event.reply("<b>Вы заблокировали этого пользователя.</b>")
                        await event.edit("<b>Пользователь приглашён успешно!</b>")


    async def kickmecmd(self, leave):
        """Используйте команду .kickme, чтобы кикнуть себя из чата."""
        args = utils.get_args_raw(leave)
        try:
            if args: await leave.edit(f"<b>До связи.\nПричина: {args}</b>")
            else: await leave.edit("<b>До связи.</b>")
            await leave.client(LeaveChannelRequest(leave.chat_id))
        except: return await leave.edit("<b>Это не чат!</b>")


    async def userscmd(self, message):
        """Команда .users <имя> выводит список всех пользователей в чате."""
        if message.chat:
            try:
                await message.edit("<b>Считаем...</b>")
                info = await message.client.get_entity(message.chat_id)
                title = info.title if info.title else "this chat"
                users = await message.client.get_participants(message.chat_id)
                mentions = f'<b>Пользователей в "{title}": {len(users)}</b> \n'
                if not utils.get_args_raw(message):
                    users = await message.client.get_participants(message.chat_id)
                    for user in users:
                        if not user.deleted:
                            mentions += f"\n• <a href =\"tg://user?id={user.id}\">{user.first_name}</a> <b>|</b> <code>{user.id}</code>"
                        else:
                            mentions += f"\n• Удалённый аккаунт <b>|</b> <code>{user.id}</code>"
                else:
                    searchq = utils.get_args_raw(message)
                    users = await message.client.get_participants(message.chat_id, search=f"{searchq}")
                    mentions = f'<b>В чате "{title}" найдено {len(users)} пользователей с именем {searchq}:</b> \n'
                    for user in users:
                        if not user.deleted:
                            mentions += f"\n• <a href =\"tg://user?id={user.id}\">{user.first_name}</a> <b>|</b> <code>{user.id}</code>"
                        else:
                            mentions += f"\n• Удалённый аккаунт <b>|</b> <code>{user.id}</code>"
            except ChatAdminRequiredError as err:
                info = await message.client.get_entity(message.chat_id)
                title = info.title if info.title else "this chat"
                users = await message.client.get_participants(message.chat_id)
                mentions = f'<b>Пользователей в "{title}": {len(users)}</b> \n'
                mentions += " " + str(err) + "\n"
        else:
            await message.edit("<b>Это не чат!</b>")
            return
        try:
            await message.edit(mentions)
        except MessageTooLongError:
            await message.edit("<b>Черт, слишком большой чат. Загружаю список пользователей в файл...</b>")
            file = open("userslist.md", "w+")
            file.write(mentions)
            file.close()
            await message.client.send_file(message.chat_id,
                                           "userslist.md",
                                           caption="<b>Пользователей в {}:</b>".format(title),
                                           reply_to=message.id)
            remove("userslist.md")
            await message.delete()


    async def adminscmd(self, message):
        """Команда .admins показывает список всех админов в чате."""
        if message.chat:
            await message.edit("<b>Считаем...</b>")
            info = await message.client.get_entity(message.chat_id)
            title = info.title if info.title else "this chat"
            admins = await message.client.get_participants(message.chat_id, filter=ChannelParticipantsAdmins)
            mentions = f'<b>Админов в "{title}": {len(admins)}</b> \n'
            for user in await message.client.get_participants(message.chat_id, filter=ChannelParticipantsAdmins):
                if not user.deleted:
                    link = f"• <a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                    userid = f"<code>{user.id}</code>"
                    mentions += f"\n{link} <b>|</b> {userid}"
                else:
                    mentions += f"\n• Удалённый аккаунт <b>|</b> <code>{user.id}</code>"
            try:
                await message.edit(mentions, parse_mode="html")
            except MessageTooLongError:
                await message.edit("Черт, слишком много админов здесь. Загружаю список админов в файл...")
                file = open("adminlist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(message.chat_id,
                                               "adminlist.md",
                                               caption="<b>Админов в \"{}\":<b>".format(title),
                                               reply_to=message.id)
                remove("adminlist.md")
                await message.delete()
        else:
            await message.edit("<b>Я слышал, что только чаты могут иметь админов...</b>")


    async def botscmd(self, message):
        """Команда .bots показывает список всех ботов в чате."""
        if message.chat:
            await message.edit("<b>Считаем...</b>")
            info = await message.client.get_entity(message.chat_id)
            title = info.title if info.title else "this chat"
            bots = await message.client.get_participants(message.to_id, filter=ChannelParticipantsBots)
            mentions = f'<b>Ботов в "{title}": {len(bots)}</b>\n'
            try:
                if isinstance(message.to_id, PeerChat):
                    await message.edit("<b>Я слышал, что только чаты могут иметь ботов...</b>")
                    return
                else:
                    async for user in message.client.iter_participants(message.chat_id, filter=ChannelParticipantsBots):
                        if not user.deleted:
                            link = f"• <a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                            userid = f"<code>{user.id}</code>"
                            mentions += f"\n{link} <b>|</b> {userid}"
                        else:
                            mentions += f"\n• Удалённый бот <b>|</b> <code>{user.id}</code>"
            except ChatAdminRequiredError as err:
                mentions += " " + str(err) + "\n"
            try:
                await message.edit(mentions, parse_mode="html")
            except MessageTooLongError:
                await message.edit(
                    "Черт, слишком много ботов здесь. Загружаю список ботов в файл...")
                file = open("botlist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(message.chat_id,
                                               "botlist.md",
                                               caption="<b>Ботов в \"{}\":</b>".format(title),
                                               reply_to=message.id)
                remove("botlist.md")
                await message.delete()
        else:
            await message.edit("<b>Я слышал, что только чаты могут иметь ботов...</b>")