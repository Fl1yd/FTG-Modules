# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
"""
Userbot module to help you manage a group
"""

from asyncio import sleep
from os import remove

from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (PeerChat, PeerChannel,
                               ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto, ChannelParticipantsBots)

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register

# =================== CONSTANT ===================
PP_TOO_SMOL = "`Картинка слишком маленькая`"
PP_ERROR = "`Сбой при обработке изображения`"
NO_ADMIN = "`Я не админ здесь!`"
NO_PERM = "`У меня нет достаточных разрешений!`"
NO_SQL = "`Запуск в режиме Non-SQL!`"

CHAT_PP_CHANGED = "`Картинка чата изменена`"
CHAT_PP_ERROR = "`Некоторые проблемы с обновлением рисунка,`" \
                "`может быть потому что я не админ здесь,`" \
                "`или не имею достаточных прав.`"
INVALID_MEDIA = "`Недействительное резрешение`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@register(outgoing=True, pattern="^\.setgpic$", groups_only=True)
async def set_group_photo(gpic):
    """ Команда .setgpic изменяет картинку группы"""
    if not gpic.is_group:
        await gpic.edit("`Я не думаю, что это чат.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await gpic.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await
                                 gpic.client.upload_file(photo)))
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


@register(outgoing=True, pattern="^\.promote(?: |$)(.*)", groups_only=True)
async def promote(promt):
    """Команда .promote повышает реплайнутого/тэгнутого пользователя"""
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(add_admins=False,
                                 invite_users=True,
                                 change_info=False,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True)

    await promt.edit("`Повышение...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        # Just in case.
        rank = "admeme"
    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("`Повышение успешно!`")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await promt.edit(NO_PERM)
        return

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#ПОВЫШЕНИЕ\n"
            f"ПОЛЬЗОВАТЕЛЬ: [{user.first_name}](tg://user?id={user.id})\n"
            f"ЧАТ: {promt.chat.title}(`{promt.chat_id}`)")


@register(outgoing=True, pattern="^\.demote(?: |$)(.*)", groups_only=True)
async def demote(dmod):
    """Команда .demote понижает реплайнутого/тэгнутого пользователя"""
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # If passing, declare that we're going to demote
    await dmod.edit("`Понижение...`")
    rank = "admeme"  # dummy rank, lol.
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return

    # New rights after demotion
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    # Edit Admin Permission
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit("`Понижение успешно!`")

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#ПОНИЖЕНИЕ\n"
            f"ПОЛЬЗОВАТЕЛЬ: [{user.first_name}](tg://user?id={user.id})\n"
            f"ЧАТ: {dmod.chat.title}(`{dmod.chat_id}`)")


@register(outgoing=True, pattern="^\.ban(?: |$)(.*)", groups_only=True)
async def ban(bon):
    """Команда .ban банит реплайнутого/тэгнутого пользователя"""
    # Here laying the sanity check
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(bon)
    if user:
        pass
    else:
        return

    # Announce that we're going to whack the pest
    await bon.edit("`Ударить вредителя!`")

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except BadRequestError:
        await bon.edit(NO_PERM)
        return
    # Helps ban group join spammers more easily
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await bon.edit(
            "`У меня нет прав на удаление сообщений! Но он все равно забанен!`")
        return
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await bon.edit(f"{user.first_name} забанен(-а)!!\
        \nID: `{str(user.id)}`\
        \nПричина: {reason}")
    else:
        await bon.edit(f"{user.first_name} забанен(-а)!!\
        \nID: `{str(user.id)}`")
    # Announce to the logging group if we have banned the person
    # successfully!
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID, "#БАН\n"
            f"ПОЛЬЗОВАТЕЛЬ: [{user.first_name}](tg://user?id={user.id})\n"
            f"ЧАТ: {bon.chat.title}(`{bon.chat_id}`)")


@register(outgoing=True, pattern="^\.unban(?: |$)(.*)", groups_only=True)
async def nothanos(unbon):
    """Команда .unban разбанит реплайнутого/тэгнутого пользователя"""
    # Here laying the sanity check
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return

    # If everything goes well...
    await unbon.edit("`Разбан...`")

    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await unbon.client(
            EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit("```Разбан успешен!```")

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID, "#РАЗБАН\n"
                f"ПОЛЬЗОВАТЕЛЬ: [{user.first_name}](tg://user?id={user.id})\n"
                f"ЧАТ: {unbon.chat.title}(`{unbon.chat_id}`)")
    except UserIdInvalidError:
        await unbon.edit("`Ох, моя логика разбана сломалась!`")


@register(outgoing=True, pattern="^\.mute(?: |$)(.*)", groups_only=True)
async def spider(spdr):
    """
    Это функция в основном приглушает писки :) 
    """
    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except AttributeError:
        await spdr.edit(NO_SQL)
        return

    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await spdr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        await spdr.edit(
            "`Руки слишком коротки, я не могу заклеить себя скотчем...\n(ヘ･_･)ヘ┳━┳`")
        return

    # If everything goes well, do announcing and mute
    await spdr.edit("`Достаю скотч!`")
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit('`Ошибка! Пользователь возможно уже в муте.`')
    else:
        try:
            await spdr.client(
                EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            # Announce that the function is done
            if reason:
                await spdr.edit(f"`Безопасно заткнут скотчем!!!`\nПричина: {reason}")
            else:
                await spdr.edit("`Безопасно заткнут скотчем!!!`")

            # Announce to logging group
            if BOTLOG:
                await spdr.client.send_message(
                    BOTLOG_CHATID, "#МУТ\n"
                    f"ПОЛЬЗОВАТЕЛЬ: [{user.first_name}](tg://user?id={user.id})\n"
                    f"ЧАТ: {spdr.chat.title}(`{spdr.chat_id}`)")
        except UserIdInvalidError:
            return await spdr.edit("`Ох, моя логика мута сломалась!`")


@register(outgoing=True, pattern="^\.unmute(?: |$)(.*)", groups_only=True)
async def unmoot(unmot):
    """Команда .unmute размутить реплайнутого/тэгнутого пользователя"""
    # Admin or creator check
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await unmot.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except AttributeError:
        await unmot.edit(NO_SQL)
        return

    # If admin or creator, inform the user and start unmuting
    await unmot.edit('```Размут...```')
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit("`Ошибка! Пользователь возможно уже не в муте.`")
    else:

        try:
            await unmot.client(
                EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit("```Размут успешен```")
        except UserIdInvalidError:
            await unmot.edit("`Ох, моя логика размута сломалась!`")
            return

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID, "#РАЗМУТ\n"
                f"ПОЛЬЗОВАТЕЛЬ: [{user.first_name}](tg://user?id={user.id})\n"
                f"ЧАТ: {unmot.chat.title}(`{unmot.chat_id}`)")


@register(incoming=True, disable_errors=True)
async def muter(moot):
    """Используется для удаления сообщений от людей в муте"""
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
    except AttributeError:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                try:
                    await moot.delete()
                    await moot.client(
                        EditBannedRequest(moot.chat_id, moot.sender_id,
                                          rights))
                except (BadRequestError, UserAdminInvalidError,
                        ChatAdminRequiredError, UserIdInvalidError):
                    await moot.client.send_read_acknowledge(
                        moot.chat_id, moot.id)
    if gmuted:
        for i in gmuted:
            if i.sender == str(moot.sender_id):
                try:
                    await moot.delete()
                except BadRequestError:
                    await moot.client.send_read_acknowledge(
                        moot.chat_id, moot.id)


@register(outgoing=True, pattern="^\.ungmute(?: |$)(.*)", groups_only=True)
async def ungmoot(un_gmute):
    """Команда .ungmute мутит пользователя во всех общих чат"""
    # Admin or creator check
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await un_gmute.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.gmute_sql import ungmute
    except AttributeError:
        await un_gmute.edit(NO_SQL)
        return
    # If pass, inform and start ungmuting
    await un_gmute.edit('```Размут...```')

    user = await get_user_from_event(un_gmute)
    user = user[0]
    if user:
        pass
    else:
        return


    if ungmute(user.id) is False:
        await un_gmute.edit("`Ошибка! Пользователь возможно не в муте.`")
    else:
        # Inform about success
        await un_gmute.edit("```Размут успешен```")

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID, "#ГЛОБАЛЬНЫЙ РАЗМУТ\n"
                f"ПОЛЬЗОВАТЕЛЬ: [{user.first_name}](tg://user?id={user.id})\n"
                f"ЧАТ: {un_gmute.chat.title}(`{un_gmute.chat_id}`)")


@register(outgoing=True, pattern="^\.gmute(?: |$)(.*)", groups_only=True)
async def gspider(gspdr):
    """Команда .gmute мутит реплайнутого/тэгнутого пользователя во всех общих чатах"""
    # Admin or creator check
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except AttributeError:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    # If pass, inform and start gmuting
    await gspdr.edit("`Хватаюсь за огромный, липкий клейкий скотч`")
    if gmute(user.id) is False:
        await gspdr.edit(
            '`Ошибка! Пользователь возмонжо уже глобально в муте.\nСкручиваю скотч.`')
    else:
        if reason:
            await gspdr.edit(f"`Глобально в муте!`Причина: {reason}")
        else:
            await gspdr.edit("`Глобально в муте!`")

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#ГЛОБАЛЬНЫЙ МУТ\n"
                f"ПОЛЬЗОВАТЕЛЬ: [{user.first_name}](tg://user?id={user.id})\n"
                f"ЧАТ: {gspdr.chat.title}(`{gspdr.chat_id}`)")


@register(outgoing=True, pattern="^\.zombies(?: |$)(.*)", groups_only=True)
async def rm_deletedacc(show):
    """Команда .delusers показывает список всех удалённых аккаунтов в чате."""
    if not show.is_group:
        await show.edit("`Я не думаю, что это чат.`")
        return
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`Нету удалённых аккаунтов, чат очищен как Ад`"

    if con != "clean":
        await show.edit("`Поиск зомби аккаунтов...`")
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"Найден(-о) **{del_u}** удаленный(-х) аккаунт(-ов) в группе,\
            \nочистите их с помощью `.zombies clean`"

        await show.edit(del_status)
        return

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await show.edit("`Я не админ здесь!`")
        return

    await show.edit("`Удаление удалённых аккаунтов...\nОх, я могу это сделать?!`")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except ChatAdminRequiredError:
                await show.edit("`У меня нету право на блокировку в этой группе`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"Удален(-о) **{del_u}** удалённый(-а) аккаунт(-ов)"

    if del_a > 0:
        del_status = f"Удален(-о) **{del_u}** удалённый(-а) аккаунт(-ов)\
        \n**{del_a}** удалённые аккаунты админов не удалены"

    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID, "#УБОРКА\n"
            f"Удален(-о) **{del_u}** удалённый(-а) аккаунт(-ов)!\
            \nЧАТ: {show.chat.title}(`{show.chat_id}`)")


@register(outgoing=True, pattern="^\.admins$", groups_only=True)
async def get_admin(show):
    """Команда .admins показывает список всех админов в чате."""
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b>Админов в {title}:</b> \n'
    try:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsAdmins):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nУдалённый аккаунт <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await show.edit(
            "Черт, слишком много админов здесь. загружаю список админов в файл...")
        file = open("adminlist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "adminlist.txt",
            caption='Админов в {}'.format(title),
            reply_to=show.id,
        )
        remove("adminlist.txt")


@register(outgoing=True, pattern="^\.bots$", groups_only=True)
async def get_bots(show):
    """Команда .bots показывает список всех ботов в чате. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b>Ботов в {title}:</b>\n'
    try:
        if isinstance(show.to_id, PeerChat):
            await show.edit("`Я слышал, что только супергруппы могут иметь ботов.`")
            return
        else:
            async for user in show.client.iter_participants(
                    show.chat_id, filter=ChannelParticipantsBots):
                if not user.deleted:
                    link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                    userid = f"<code>{user.id}</code>"
                    mentions += f"\n{link} {userid}"
                else:
                    mentions += f"\nУдалённых ботов <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await show.edit(
            "Черт, слишком много ботов здесь. Загружаю список ботов в файл.")
        file = open("botlist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "botlist.txt",
            caption='Bots in {}'.format(title),
            reply_to=show.id,
        )
        remove("botlist.txt")


@register(outgoing=True, pattern="^\.pin(?: |$)(.*)", groups_only=True)
async def pin(msg):
    """Команда .pin закрепляет реплайнутое/тэгнутое сообщение в чате."""
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit("`Ответь на сообщение чтобы закрепить его.`")
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await msg.edit(NO_PERM)
        return

    await msg.edit("`Закреплено успешно!`")

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID, "#ЗАКРЕП\n"
            f"АДМИН: [{user.first_name}](tg://user?id={user.id})\n"
            f"ЧАТ: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"ГРОМКИЙ(?, хз чеза перевод): {not is_silent}")


@register(outgoing=True, pattern="^\.kick(?: |$)(.*)", groups_only=True)
async def kick(usr):
    """Команда .kick кикает реплайнутого/тэгнутого пользователя. """
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.edit("`Не могу кикнуть пользователя.`")
        return

    await usr.edit("`Кик...`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except Exception as e:
        await usr.edit(NO_PERM)
        return

    if reason:
        await usr.edit(
            f"`Кикнут` [{user.first_name}](tg://user?id={user.id})`!`\nПричина: {reason}"
        )
    else:
        await usr.edit(
            f"`Кикнут` [{user.first_name}](tg://user?id={user.id})`!`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID, "#КИК\n"
            f"ПОЛЬЗОВАТЕЛЬ: [{user.first_name}](tg://user?id={user.id})\n"
            f"ЧАТ: {usr.chat.title}(`{usr.chat_id}`)\n")


@register(outgoing=True, pattern="^\.users ?(.*)", groups_only=True)
async def get_users(show):
    """Команда .users показывает список всех пользователей в чате."""
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = 'Пользователей в {}: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nУдалённый аккаунт`{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nУдалённый аккаунт `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Черт, слишком большой чат, загружаю список пользователей в файл.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption='Пользователей в {}'.format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """Получаю пользователя с аргумента или реплайнутого сообщения."""
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Введите юзернейм пользователя, ID или реплай!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj


CMD_HELP.update({
    "admin":
    ".promote <username/userid> : <пользовательский ранг (по желанию)> (или) реплай на сообщение с .promote <ранк (по желанию)>\
\nИспользование: Повышает в правах админа пользователя в чате.\
\n\n.demote <username/userid> (или) реплай на сообщение с .demote\
\nИспользование: Аннулировать административные права пользователя в чате.\
\n\n.ban <username/userid> : <причина (по желанию)> (или) реплай на сообщение с .ban <причина (по желанию)>\
\nИспользование: Банит пользователя в чате.\
\n\n.unban <username/userid> (или) реплай на сообщение с .unban\
\nИспользование: Разбан пользователя в чате.\
\n\n.mute <username/userid> : <причина (по желанию)> реплай на сообщение с .mute <причина (по желанию)>\
\nИспользование: Мутит пользователя в чате, работает на админах тоже.\
\n\n.unmute <username/userid> (или) реплай на сообщние с .unmute\
\nПользование: Размут пользователя в чате.\
\n\n.gmute <username/userid> : <причина (по желанию)> (или) реплай на сообщение с .gmute <причина (по желанию)>\
\nИспользование: Мутит пользователя во всех общих чатах.\
\n\n.ungmute <username/userid> (или) реплай на сообщение с .ungmute\
\nИспользование: Размут пользователя во всех общих чатах.\
\n\n.delusers\
\nИспользование: Удаляет все удалённые аккаунты в чате.\
\n\n.admins\
\nИспользование: Список всех админов в чате.\
\n\n.bots\
\nИспользование: Список всех ботов в чате.\
\n\n.users или .users <определённый запрос>\
\nИспользование: Список всех (или определённых) пользователей в чате\
\n\n.setgpic <реплай на картинку>\
\nИспользование: Изменяет картинку группы."
})
