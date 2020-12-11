from .. import loader, utils
from telethon.tl.functions.messages import GetCommonChatsRequest
from telethon.tl.functions.users import GetFullUserRequest


def register(cb):
    cb(GetCommonChatsMod())

class GetCommonChatsMod(loader.Module):
    """Общие чаты с пользователем."""
    strings = {'name': 'GetCommonChats'}

    async def commoncmd(self, message):
        """Используй .common <@ или реплай>, чтобы узнать общие чаты с пользователем."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args and not reply:
            return await message.edit('<b>Нет аргументов или реплая.</b>')
        await message.edit('<b>Считаем...</b>')
        try:
            if args:
                if args.isnumeric():
                    user = int(args)
                    user = await message.client.get_entity(user)
                else:
                    user = await message.client.get_entity(args) 
            else: 
                user = await utils.get_user(reply)
        except ValueError:
            return await message.edit('<b>Не удалось найти пользователя.</b>')
        msg = f'<b>Общие чаты с {user.first_name}:</b>\n'
        user = await message.client(GetFullUserRequest(user.id))
        comm = await message.client(GetCommonChatsRequest(user_id=user.user.id, max_id=0, limit=100))
        count = 0
        m = ''
        for chat in comm.chats:
            m += f'\n• <a href="tg://resolve?domain={chat.username}">{chat.title}</a> <b>|</b> <code>{chat.id}</code>'
            count += 1
        msg = f'<b>Общие чаты с {user.user.first_name}: {count}</b>\n'
        await message.edit(f'{msg} {m}')