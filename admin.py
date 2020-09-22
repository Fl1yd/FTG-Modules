# Admin Tools for Friendly-Telegram UserBot.
# Copyright (C) 2020 @Fl1yd, @AtiksX.
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

import io
import logging
import time
from .. import loader, utils, security
from io import BytesIO
from PIL import Image
from asyncio import sleep
from telethon.errors import (ChatAdminRequiredError, UserAdminInvalidError, FloodWaitError, PhotoCropSizeSmallError)
from telethon.tl.types import (ChatAdminRights, ChatBannedRights)
from telethon.tl.functions.channels import (EditAdminRequest, EditBannedRequest, EditPhotoRequest)
from telethon.tl.functions.messages import (UpdatePinnedMessageRequest, EditChatAdminRequest)
logger = logging.getLogger(__name__)

# ================== КОНСТАНТЫ ========================

PROMOTE_RIGHTS = ChatAdminRights(post_messages=True,
                                 add_admins=None,
                                 invite_users=True,
                                 change_info=None,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True,
                                 edit_messages=True)

DEMOTE_RIGHTS = ChatAdminRights(post_messages=None,
                                add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None,
                                edit_messages=None)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None,
                                 view_messages=None,
                                 send_messages=False,
                                 send_media=False,
                                 send_stickers=False,
                                 send_gifs=False,
                                 send_games=False,
                                 send_inline=False,
                                 embed_links=False)

BANNED_RIGHTS = ChatBannedRights(until_date=None,
                                 view_messages=True,
                                 send_messages=True,
                                 send_media=True,
                                 send_stickers=True,
                                 send_gifs=True,
                                 send_games=True,
                                 send_inline=True,
                                 embed_links=True)

UNBAN_RIGHTS = ChatBannedRights(until_date=None,
                                view_messages=None,
                                send_messages=None,
                                send_media=None,
                                send_stickers=None,
                                send_gifs=None,
                                send_games=None,
                                send_inline=None,
                                embed_links=None)

# =====================================================

def register(cb):
    cb(AdminToolsMod())

class AdminToolsMod(loader.Module):
    """Администрирование чата"""
    strings = {'name': 'AdminTools',
               'no_reply': '<b>Нет реплая на картинку/стикер.</b>',
               'not_pic': '<b>Это не картинка/стикер</b>',
               'wait': '<b>Минуточку...</b>',
               'pic_so_small': '<b>Картинка слишком маленькая, попробуйте другую.</b>',
               'pic_changed': '<b>Картинка чата изменена.</b>',
               'promote_none': '<b>Некого повышать.</b>',
               'who': '<b>Кто это?</b>',
               'not_admin': '<b>Я здесь не админ.</b>',
               'promoted': '<b>{} повышен в правах администратора.</b>',
               'wtf_is_it': '<b>Что это?</b>',
               'this_isn`t_a_chat': '<b>Это не чат!</b>',
               'demote_none': '<b>Некого понижать.</b>',
               'demoted': '<b>{} понижен в правах администратора.</b>',
               'pinning': '<b>Пин...</b>',
               'pin_none': '<b>Ответь на сообщение чтобы закрепить его.</b>',
               'unpinning': '<b>Анпин...</b>',
               'unpin_none': '<b>Нечего откреплять.</b>',
               'no_rights': '<b>У меня нет прав.</b>',
               'pinned': '<b>Закреплено успешно!</b>',
               'unpinned': '<b>Откреплено успешно!</b>',
               'can`t_kick': '<b>Не могу кикнуть пользователя.</b>',
               'kicking': '<b>Кик...</b>',
               'kick_none': '<b>Некого кикать.</b>',
               'kicked': '<b>{} кикнут из чата.</b>',
               'banned': '<b>{} забанен в чате.</b>',
               'ban_none': '<b>Некому давать бан.</b>',
               'unban_none': '<b>Некого разбанить.</b>',
               'unbanned': '<b>{} разбанен в чате.</b>',
               'mute_none': '<b>Некому давать мут.</b>',
               'muted': '<b>{} теперь в муте на </b>',
               'no_aargs': '<b>Неверно указаны аргументы.</b>',
               'unmute_none': '<b>Некого размутить.</b>',
               'unmuted': '<b>{} теперь не в муте.</b>',
               'del_u_search': '<b>Поиск удалённых аккаунтов...</b>',
               'del_u_kicking': '<b>Кик удалённых аккаунтов...\nОх~, я могу это сделать?!</b>'}

    async def client_ready(self, client, db):
        self.client = client


    async def ecpcmd(self, gpic):
        """Команда .ecp изменяет картинку чата.\nИспользование: .ecp <реплай на картинку/стикер>."""
        if gpic.chat:
            try:
                replymsg = await gpic.get_reply_message()
                chat = await gpic.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    await utils.answer(gpic, self.strings('not_admin', gpic))
                    return
                if not replymsg:
                    await utils.answer(gpic, self.strings('no_reply', gpic))
                    return
                else:
                    pic = await check_media(gpic, replymsg)
                    if not pic:
                        await utils.answer(gpic, self.strings('not_pic', gpic))
                        return
                await utils.answer(gpic, self.strings('wait', gpic))
                what = resize(pic)
                if what:
                    try:
                        await gpic.client(EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(what)))
                    except PhotoCropSizeSmallError:
                        await utils.answer(gpic, self.strings('pic_so_small', gpic))
                        return
                await utils.answer(gpic, self.strings('pic_changed', gpic))
            except:
                await utils.answer(gpic, self.strings('no_rights', gpic))
                return
        else:
            await utils.answer(gpic, self.strings('this_isn`t_a_chat', gpic))
            return


    async def promotecmd(self, promt):
        """Команда .promote повышает пользователя в правах администратора.\nИспользование: .promote <@ или реплай>."""
        if promt.chat:
            try:
                chat = await promt.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    await utils.answer(promt, self.strings('not_admin', promt))
                    return
                if promt.is_reply:
                    user = await utils.get_user(await promt.get_reply_message())
                else:
                    args = utils.get_args(promt)
                    if not args:
                        return await utils.answer(promt, self.strings('promote_none', promt))
                    user = await self.client.get_entity(args[0])
                if not user:
                    return await utils.answer(promt, self.strings('who', promt))
                rank = utils.get_args_raw(promt)
                if not rank:
                    rank = "одмэн"
                logger.debug(user)
                try:
                    if promt.is_channel:
                        await self.client(EditAdminRequest(promt.chat_id, user.id, PROMOTE_RIGHTS, rank))
                except:
                    await utils.answer(promt, self.strings('no_rights', promt))
                else:
                    await self.allmodules.log("promote", group=promt.chat_id, affected_uids=[user.id])
                    await utils.answer(promt,
                                       self.strings('promoted', promt).format(utils.escape_html(user.first_name)))
            except FloodWaitError as e:
                await promt.edit('<b>Флудвейт {} секунд вызван ошибкой "Изменение информации".</b>'.format(e.seconds))
                return
            except:
                await utils.answer(promt, self.strings('wtf_is_it', promt))
                return
        else:
            await utils.answer(promt, self.strings('this_isn`t_a_chat', promt))
            return

    async def demotecmd(self, demt):
        """Команда .demote понижает пользователя в правах администратора.\nИспользование: .demote <@ или реплай>."""
        if demt.chat:
            try:
                chat = await demt.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    await utils.answer(demt, self.strings('not_admin', demt))
                    return
                if demt.is_reply:
                    user = await utils.get_user(await demt.get_reply_message())
                else:
                    args = utils.get_args(demt)
                    if not args:
                        return await utils.answer(demt, self.strings('demote_none', demt))
                    user = await self.client.get_entity(args[0])
                if not user:
                    return await utils.answer(demt, self.strings('who', demt))
                logger.debug(user)
                try:
                    if demt.is_channel:
                        await self.client(EditAdminRequest(demt.chat_id, user.id, DEMOTE_RIGHTS, ""))
                    else:
                        await self.client(EditChatAdminRequest(demt.chat_id, user.id, False))
                except:
                    await utils.answer(demt, self.strings('no_rights', demt))
                else:
                    await self.allmodules.log("demote", group=demt.chat_id, affected_uids=[user.id])
                    await utils.answer(demt, self.strings('demoted', demt).format(utils.escape_html(user.first_name)))
            except FloodWaitError as e:
                await demt.edit('<b>Флудвейт {} секунд вызван ошибкой "Изменение информации".</b>'.format(e.seconds))
                return
            except:
                await utils.answer(demt, self.strings('wtf_is_it'))
                return
        else:
            await utils.answer(demt, self.strings('this_isn`t_a_chat', demt))
            return


    async def pincmd(self, pint):
        """Команда .pin закрепляет сообщение в чате.\nИспользование: .pin <реплай>."""
        if pint.chat:
            try:
                to_pin = pint.reply_to_msg_id
                is_silent = True

                await utils.answer(pint, self.strings('pinning', pint))
                await sleep(0.1)

                if not to_pin:
                    await utils.answer(pint, self.strings('pin_none', pint))
                    return

                try:
                    await pint.client(UpdatePinnedMessageRequest(pint.to_id, to_pin, is_silent))
                except:
                    await utils.answer(pint, self.strings('no_rights', pint))
                    return
                await utils.answer(pint, self.strings('pinned', pint))
            except FloodWaitError as e:
                await pint.edit('<b>Флудвейт {} секунд вызван ошибкой "Изменение информации".</b>'.format(e.seconds))
                return
        else:
            await utils.answer(pint, self.strings('this_isn`t_a_chat', pint))


    async def unpincmd(self, unpon):
        """Команда .unpin открепляет закрепленное сообщение в чате.\nИспользование: .unpin."""
        if unpon.chat:
            try:
                await utils.answer(unpon, self.strings('unpinning', unpon))
                await sleep(0.1)

                try:
                    await self.client.pin_message(unpon.chat, message=None, notify=None)
                except ChatAdminRequiredError:
                    await utils.answer(unpon, self.strings('no_rights', unpon))
                    return

                await utils.answer(unpon, self.strings('unpinned', unpon))
            except FloodWaitError as e:
                await unpon.edit('<b>Флудвейт {} секунд вызван ошибкой "Изменение информации".</b>'.format(e.seconds))
                return
            except:
                await utils.answer(unpon, self.strings('unpin_none', unpon))
                return
        else:
            await utils.answer(unpon, self.strings('this_isn`t_a_chat', unpon))


    async def kickcmd(self, kock):
        """Команда .kick кикает пользователя.\nИспользование: .kick <@ или реплай>."""
        if kock.chat:
            try:
                chat = await kock.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    await utils.answer(kock, self.strings('not_admin', kock))
                    return
                if kock.is_reply:
                    user = await utils.get_user(await kock.get_reply_message())
                else:
                    args = utils.get_args(kock)
                    if not args:
                        return await utils.answer(kock, self.strings('kick_none', kock))
                    user = await self.client.get_entity(args[0])
                if not user:
                    return await utils.answer(kock, self.strings('who', kock))
                logger.debug(user)
                if user.is_self:
                    if not (await kock.client.is_bot()
                            or await self.allmodules.check_security(kock, security.OWNER | security.SUDO)):
                        return
                try:
                    await utils.answer(kock, self.strings('kicking', kock))
                    await self.client.kick_participant(kock.chat_id, user.id)
                except:
                    await utils.answer(kock, self.strings('no_rights', kock))
                else:
                    await self.allmodules.log("kick", group=kock.chat_id, affected_uids=[user.id])
                    await utils.answer(kock, self.strings('kicked', kock).format(utils.escape_html(user.first_name)))
            except FloodWaitError as e:
                await kock.edit('<b>Флудвейт {} секунд вызван ошибкой "Изменение информации".</b>'.format(e.seconds))
                return
            except:
                await utils.answer(kock, self.strings('wtf_is_it', kock))
        else:
            await utils.answer(kock, self.strings('this_isn`t_a_chat', kock))


    async def bancmd(self, bon):
        """Команда .ban даёт бан пользователю.\nИспользование: .ban <@ или реплай>."""
        if bon.chat:
            try:
                chat = await bon.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    await utils.answer(bon, self.strings('not_admin', bon))
                    return
                if bon.is_reply:
                    user = await utils.get_user(await bon.get_reply_message())
                else:
                    args = utils.get_args(bon)
                    if not args:
                        return await utils.answer(bon, self.strings('ban_none', bon))
                    user = await self.client.get_entity(args[0])
                if not user:
                    return await utils.answer(bon, self.strings('who', bon))
                logger.debug(user)
                try:
                    await self.client(EditBannedRequest(bon.chat_id, user.id,
                                                        ChatBannedRights(until_date=None, view_messages=True)))
                except:
                    await utils.answer(bon, self.strings('no_rights', bon))
                else:
                    await self.allmodules.log("ban", group=bon.chat_id, affected_uids=[user.id])
                    await utils.answer(bon, self.strings('banned', bon).format(utils.escape_html(user.first_name)))
            except FloodWaitError as e:
                await bon.edit('<b>Флудвейт {} секунд вызван ошибкой "Изменение информации".</b>'.format(e.seconds))
                return
            except:
                await utils.answer(bon, self.strings('wtf_is_it', bon))
        else:
            await utils.answer(bon, self.strings('this_isn`t_a_chat', bon))


    async def unbancmd(self, unbon):
        """Команда .unban для разбана пользователя.\nИспользование: .unban <@ или реплай>."""
        if unbon.chat:
            try:
                chat = await unbon.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    await utils.answer(unbon, self.strings('not_admin', unbon))
                    return
                if unbon.is_reply:
                    user = await utils.get_user(await unbon.get_reply_message())
                else:
                    args = utils.get_args(unbon)
                    if not args:
                        return await utils.answer(unbon, self.strings('unban_none', unbon))
                    user = await self.client.get_entity(args[0])
                if not user:
                    return await utils.answer(unbon, self.strings('who', unbon))
                logger.debug(user)
                try:
                    await self.client(EditBannedRequest(unbon.chat_id, user.id,
                                                        ChatBannedRights(until_date=None, view_messages=False)))
                except:
                    await utils.answer(unbon, self.strings('no_rights', unbon))
                else:
                    await self.allmodules.log("unban", group=unbon.chat_id, affected_uids=[user.id])
                    await utils.answer(unbon,
                                       self.strings('unbanned', unbon).format(utils.escape_html(user.first_name)))
            except FloodWaitError as e:
                await unbon.edit('<b>Флудвейт {} секунд вызван ошибкой "Изменение информации".</b>'.format(e.seconds))
                return
            except:
                await utils.answer(unbon, self.strings('wtf_is_it', unbon))
        else:
            await utils.answer(unbon, self.strings('this_isn`t_a_chat', unbon))


    async def mutecmd(self, mot):
        """Команда .mute даёт мут пользователю.\nИспользование: .mute <@ или реплай> <время (1m, 1h, 1d)>."""
        if mot.chat:
            try:
                chat = await mot.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    await utils.answer(mot, self.strings('not_admin', mot))
                    return
                if mot.is_reply:
                    user = await utils.get_user(await mot.get_reply_message())

                else:
                    who = utils.get_args_raw(mot).split(' ')
                    user = await mot.client.get_entity(who[0])

                    if len(who) == 1:
                        timee = ChatBannedRights(until_date=True, send_messages=True)
                        await mot.client(EditBannedRequest(mot.chat_id, user.id, timee))
                        await mot.edit('<b>{} теперь в муте.</b>'.format(user.first_name))
                        return

                    if not user:
                        return await utils.answer(mot, self.strings('mute_none', mot))
                    if user:
                        tim = who[1]
                        if tim:
                            if len(tim) != 2:
                                return await utils.answer(mot, self.strings('no_aargs', mot))
                            num = ''
                            t = ''
                            for q in tim:
                                if q.isdigit():
                                    num += q
                                else:
                                    t += q

                            text = f'<b>{num}'
                            if t == 'm':
                                num = int(num) * 60
                                text += ' минут(-ы).</b>'
                            elif t == 'h':
                                num = int(num) * 3600
                                text += ' час(-а/-ов).</b>'
                            elif t == 'd':
                                num = int(num) * 86400
                                text += ' дня(-ей) .</b>'
                            else:
                                return await utils.answer(mot, self.strings('no_aargs', mot))
                            timee = ChatBannedRights(until_date=time.time() + int(num), send_messages=True)
                            try:
                                await mot.client(EditBannedRequest(mot.chat_id, user.id, timee))
                                await utils.answer(mot, self.strings('muted', mot).format(utils.escape_html(user.first_name)) + text)
                                return
                            except:
                                await utils.answer(mot, self.strings('no_rights', mot))
                        else:
                            timee = ChatBannedRights(until_date=True, send_messages=True)
                            await mot.client(EditBannedRequest(mot.chat_id, user.id, timee))
                            await mot.edit('<b>{} теперь в муте.</b>'.format(user.first_name))
                            return

                logger.debug(user)
                tim = utils.get_args(mot)
                if tim:
                    if len(tim[0]) < 2:
                        return await utils.answer(mot, self.strings('no_aargs', mot))
                    num = ''
                    t = ''
                    for q in tim[0]:
                        if q.isdigit():
                            num += q
                        else:
                            t += q

                    text = f'<b>{num}'
                    if t == 'm':
                        num = int(num) * 60
                        text += ' минут(-ы).</b>'
                    elif t == 'd':
                        num = int(num) * 86400
                        text += ' дня(-ей) .</b>'
                    elif t == 'h':
                        num = int(num) * 3600
                        text += ' час(-а/-ов).</b>'
                    else:
                        return await utils.answer(mot, self.strings('no_aargs', mot))
                    timee = ChatBannedRights(until_date=time.time() + int(num), send_messages=True)
                    try:
                        await mot.client(EditBannedRequest(mot.chat_id, user.id, timee))
                        await utils.answer(mot, self.strings('muted', mot).format(utils.escape_html(user.first_name)) + text)
                        return
                    except:
                        await utils.answer(mot, self.strings('no_rights', mot))
                else:
                    timee = ChatBannedRights(until_date=True, send_messages=True)
                    await mot.client(EditBannedRequest(mot.chat_id, user.id, timee))
                    await mot.edit('<b>{} теперь в муте.</b>'.format(user.first_name))
                    return
            except:
                await utils.answer(mot, self.strings('mute_none', mot))
                return
        else:
            await utils.answer(mot, self.strings('this_isn`t_a_chat', mot))


    async def unmutecmd(self, unmot):
        """Команда .unmute для размута пользователя.\nИспользование: .unmute <@ или реплай>."""
        if unmot.chat:
            try:
                chat = await unmot.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    await utils.answer(unmot, self.strings('not_admin', unmot))
                    return
                if unmot.is_reply:
                    user = await utils.get_user(await unmot.get_reply_message())
                else:
                    args = utils.get_args(unmot)
                    if not args:
                        return await utils.answer(unmot, self.strings('unmute_none', unmot))
                    user = await self.client.get_entity(args[0])
                if not user:
                    return await utils.answer(unmot, self.strings('who', unmot))
                logger.debug(user)
                try:
                    await self.client(EditBannedRequest(unmot.chat_id, user.id, UNMUTE_RIGHTS))
                except:
                    await utils.answer(unmot, self.strings('not_admin', unmot))
                else:
                    await self.allmodules.log("unmute", group=unmot.chat_id, affected_uids=[user.id])
                    await utils.answer(unmot, self.strings('unmuted', unmot).format(utils.escape_html(user.first_name)))
            except FloodWaitError as e:
                await unmot.edit('<b>Флудвейт {} секунд вызван ошибкой "Изменение информации".</b>'.format(e.seconds))
                return
            except:
                await utils.answer(unmot, self.strings('wtf_is_it', unmot))
        else:
            await utils.answer(unmot, self.strings('this_isn`t_a_chat', unmot))


    async def deluserscmd(self, delus):
        """Команда .delusers показывает список всех удалённых аккаунтов в чате.\nИспользование: .delusers (clean)."""
        if not delus.is_group:
            await utils.answer(delus, self.strings('this_isn`t_a_chat', delus))
            return
        try:
            con = utils.get_args_raw(delus)
            del_u = 0
            del_status = '<b>Нет удалённых аккаунтов, чат очищен.</b>'

            if con != "clean":
                await utils.answer(delus, self.strings('del_u_search', delus))
                async for user in delus.client.iter_participants(delus.chat_id):
                    if user.deleted:
                        del_u += 1
                        await sleep(1)

                if del_u == 1:
                    del_status = f"<b>Найден {del_u} удаленный аккаунт в чате, очистите их с помощью </b><code>.delusers clean</code><b>.</b>"
                if del_u > 0:
                    del_status = f"<b>Найдено {del_u} удаленных аккаунтов в чате, очистите их с помощью </b><code>.delusers clean</code><b>.</b>"

                await delus.edit(del_status)
                return

            chat = await delus.get_chat()
            admin = chat.admin_rights
            creator = chat.creator
            if not admin and not creator:
                await utils.answer(delus, self.strings('not_admin', delus))
                return

            await utils.answer(delus, self.strings('del_u_kicking', delus))
            del_u = 0
            del_a = 0

            async for user in delus.client.iter_participants(delus.chat_id):
                if user.deleted:
                    try:
                        await delus.client(EditBannedRequest(delus.chat_id, user.id, BANNED_RIGHTS))
                    except ChatAdminRequiredError:
                        await utils.answer(delus, self.strings('no_rights', delus))
                        return
                    except UserAdminInvalidError:
                        del_u -= 1
                        del_a += 1
                    await delus.client(EditBannedRequest(delus.chat_id, user.id, UNBAN_RIGHTS))
                    del_u += 1

            if del_u == 1:
                del_status = f"<b>Кикнут {del_u} удалённый аккаунт.</b>"
            if del_u > 0:
                del_status = f"<b>Кикнуто {del_u} удалённых аккаунтов.</b>"

            if del_a == 1:
                del_status = f"<b>Кикнут {del_u} удалённый аккаунт.\n" \
                             f"{del_a} удалённый аккаунт админа не кикнут.</b>"
            if del_a > 0:
                del_status = f"<b>Кикнуто {del_u} удалённых аккаунтов.\n" \
                             f"{del_a} удалённых аккаунта админов не кикнуты.</b>"

            await delus.edit(del_status)
        except FloodWaitError as e:
            await delus.edit('<b>Кикнуто {} удалённых аккаунтов.\n'
                             'Флудвейт {} секунд вызван ошибкой "Изменение информации".</b>'.format(del_u, e.seconds))
            return


def resize(reply):
    smth = Image.open(BytesIO(reply))
    smth = smth.resize((512, 512))
    out = io.BytesIO()
    out.name = "outsider.png"
    smth.save(out)
    return out.getvalue()

async def check_media(message, reply):
    if reply and reply.media:
        if reply.photo:
            data = reply.photo
        elif reply.document:
            if reply.gif or reply.video or reply.audio or reply.voice:
                return None
            data = reply.media.document
        else:
            return None
    else:
        return None
    if not data or data is None:
        return None
    else:
        data = await message.client.download_file(data, bytes)
        try:
            Image.open(io.BytesIO(data))
            return data
        except:
            return None