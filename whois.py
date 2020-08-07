# -*- coding: utf-8 -*-

import logging
import io
from .. import loader, utils
import telethon

logger = logging.getLogger(__name__)


def register(cb):
    cb(WhoIsMod())

@loader.tds
class WhoIsMod(loader.Module):
    """Получает информацию о пользователе в Телеграме (включая вас!)."""
    strings = {"name": "WhoIs"}
    
    async def client_ready(self, client, db):
        self.client = client
    
    async def whoiscmd(self, message):
        reply = await message.get_reply_message()
        if not reply:
            reply = message
        profile_photo_url = reply.from_id
        profile_type = "Пользователь"

        if isinstance(reply.to_id, telethon.tl.types.PeerChannel) and reply.fwd_from:
            user = reply.forward.chat
        elif isinstance(reply.to_id, telethon.tl.types.PeerChat):
            chat = await self.client(telethon.tl.functions.messages.GetFullChatRequest(reply.to_id))
            participants = chat.full_chat.participants.participants
            participant = next(filter(lambda x: x.user_id == reply.from_id, participants), None)
            user = await reply.get_sender()
        else:
            user = await reply.get_sender()

        username = telethon.utils.get_display_name(user)
        user_id = reply.from_id

        if reply.fwd_from:
            if reply.fwd_from.saved_from_peer:
                profile_photo_url = reply.forward.chat
                profile_type = "Канал"
            elif reply.fwd_from.from_name:
                username = reply.fwd_from.from_name
                profile_photo_url = None
            elif reply.forward.sender:
                username = telethon.utils.get_display_name(reply.forward.sender)
                profile_photo_url = reply.forward.sender.id
            elif reply.forward.chat:
                profile_type = "Канал"
                profile_photo_url = user
        else:
            if isinstance(reply.to_id, telethon.tl.types.PeerUser) is False:
                try:
                    user = await self.client(telethon.tl.functions.channels.GetParticipantRequest(message.chat_id,
                                                                                                  user))
                    if isinstance(user.participant, telethon.tl.types.ChannelParticipantCreator):
                        admintitle = user.participant.rank or self.strings("creator", message)
                    elif isinstance(user.participant, telethon.tl.types.ChannelParticipantAdmin):
                        admintitle = user.participant.rank or self.strings("admin", message)
                    user = user.users[0]
                except telethon.errors.rpcerrorlist.UserNotParticipantError:
                    pass
        profile_photo = io.BytesIO()
        is_pfp = False
        if profile_photo_url is not None:
            await self.client.download_profile_photo(profile_photo_url, profile_photo)
            profile_photo.seek(0)
            is_pfp = True
        
        pfp_count = 0
        is_bot = False
        verified = False
        bio = None
        is_restricted = False
        common_chats = 0
        
        if profile_type == "Пользователь":
            user = await self.client(
                telethon.tl.functions.users.GetFullUserRequest(reply.from_id))
            profile_photos = await self.client(
                telethon.tl.functions.photos.GetUserPhotosRequest(user_id=user.user.id,
                                                                  offset=42,
                                                                  max_id=0,
                                                                  limit=80))
            try:
                pfp_count = profile_photos.count
            except AttributeError:
                pass
            is_bot = user.user.bot
            verified = user.user.verified
            is_restricted = user.user.restricted
            bio = user.about
            common_chats = user.common_chats_count
 
        bio = "У пользователя нету информации о себе." if not bio else bio
        
        msg = "<b>ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ:</b>\n\n"
        msg += "Имя: {}\n".format(username)
        msg += "Юзернейм: {}\n".format("@" + user.user.username if profile_type == "Пользователь" else "")
        msg += "Кол-во аватарок: {}\n".format(pfp_count)
        msg += "Бот?: {}\n".format(is_bot)
        msg += "Есть ограничения?: {}\n".format(is_restricted)
        msg += "Верифицирован?: {}\n".format(verified)
        msg += "ID: <code>{}</code>\n\n".format(user_id)
        msg += "О себе:\n<code>{}</code>\n\n".format(bio)
        msg += "Тип профиля: <code>{}</code>\n".format(profile_type)
        msg += "Общие чаты: {}\n".format(common_chats)
        msg += "Пермалинк: {}".format(f"<a href=\"tg://user?id={user_id}\">клик</a>")
        
        if is_pfp:
            await utils.answer(message, profile_photo, caption=msg)
        else:
            await utils.answer(message, msg)
    