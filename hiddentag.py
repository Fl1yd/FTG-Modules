from .. import loader, utils
from telethon.tl.functions.users import GetFullUserRequest


def register(cb):
    cb(HiddenTagMod())

class HiddenTagMod(loader.Module):
    """Скрытно тегнуть пользователя."""
    strings = {'name': 'HiddenTag'}

    async def tagcmd(self, message):
        """Использование: .tag <@> <текст (по желанию)>."""
        args = utils.get_args_raw(message).split(' ')
        reply = await message.get_reply_message()
        user = None
        tag = None
        try:
            if len(args) == 1:
                args = utils.get_args_raw(message)
                if args.isnumeric():
                    user = int(args)
                    user = await message.client.get_entity(user)
                else:
                    user = await message.client.get_entity(args)
                tag = 'говно залупное\n                пашет.'
            elif len(args) >= 2:
                if args[0].isnumeric():
                    user = int(args[0])
                    user = await message.client.get_entity(user)
                else:
                    user = await message.client.get_entity(args[0])
                tag = utils.get_args_raw(message).split(' ', 1)[1]
        except:
            return await message.edit("Не удалось найти пользователя.")
        await message.delete()
        user = await message.client(GetFullUserRequest(user.id))
        await message.client.send_message(message.to_id, f'{tag} <a href="tg://user?id={user.user.id}">\u2060</a>', reply_to=reply.id if reply else None)