import logging
import inspect
from telethon.tl.functions.channels import JoinChannelRequest
from .. import loader, utils, main, security
logger = logging.getLogger(__name__)


@loader.tds
class HelpMod(loader.Module):
    """Описание этого модуля."""
    strings = {'name': 'CustomHelp',
               'bad_module': '<b>Указано неверное название модуля.</b>',
               'single_mod_header': '<b>Справка к</b> <u>{}</u>:\n',
               'single_cmd': '\n➜ <code><u>{}</u></code>\n    ╰',
               'undoc_cmd': 'Для этой команды нет описания.\n',
               'all_header': '<b>Список из {} доступных модулей:</b>\n',
               'mod_tmpl': '\n➜ <b>{}</b>',
               'first_cmd_tmpl': ': <code>{}</code>',
               'cmd_tmpl': ', <code>{}</code>',
               'joined': '<b>Уже вступил в <a href="https://t.me/ftgmodulesbyfl1yd">канал</a> авторских модулей</b>',
               'join': '<b>Вступить в <a href="https://t.me/ftgmodulesbyfl1yd">канал</a> авторских модулей</b>'}

    @loader.unrestricted
    async def helpcmd(self, message):
        """.help <название модуля>."""
        args = utils.get_args_raw(message)
        if args:
            module = None
            for mod in self.allmodules.modules:
                if mod.strings('name', message).lower() == args.lower():
                    module = mod
            if module is None:
                await utils.answer(message, self.strings('bad_module', message))
                return
            try:
                name = module.strings('name', message)
            except KeyError:
                name = getattr(module, 'name', 'ERROR')
            reply = self.strings('single_mod_header', message).format(utils.escape_html(name),
                                                                      utils.escape_html((self.db.get(main.__name__,
                                                                                                     'command_prefix',
                                                                                                     False) or '.')[0]))
            if module.__doc__:
                reply += '\n' + '\n'.join('' + t for t in utils.escape_html(inspect.getdoc(module)).split('\n'))
            else:
                logger.warning('У модуля %s отсутствует описание!', module)
            commands = {name: func for name, func in module.commands.items()
                        if await self.allmodules.check_security(message, func)}
            for name, fun in commands.items():
                reply += self.strings('single_cmd', message).format(name)
                if fun.__doc__:
                    reply += utils.escape_html('\n'.join('  ' + t for t in inspect.getdoc(fun).split('\n')))
                else:
                    reply += self.strings('undoc_cmd', message)
        else:
            count = 0
            for i in self.allmodules.modules:
                if len(i.commands) != 0:
                    count += 1
            reply = self.strings('all_header', message).format(count)
            for mod in self.allmodules.modules:
                try:
                    name = mod.strings('name', message)
                except KeyError:
                    name = getattr(mod, 'name', 'ERROR')
                reply += self.strings('mod_tmpl', message).format(name)
                first = True
                commands = [name for name, func in mod.commands.items()
                            if await self.allmodules.check_security(message, func)]
                for cmd in commands:
                    if first:
                        reply += self.strings('first_cmd_tmpl', message).format(cmd)
                        first = False
                    else:
                        reply += self.strings('cmd_tmpl', message).format(cmd)
                reply += '</code>'
        await utils.answer(message, reply)

    @loader.unrestricted
    async def supportcmd(self, message):
        """Вступить в канал авторских модулей."""
        if not self.is_bot and await self.allmodules.check_security(message, security.OWNER | security.SUDO):
            await self.client(JoinChannelRequest('https://t.me/ftgmodulesbyfl1yd'))
            await utils.answer(message, self.strings('joined', message))
        else:
            await utils.answer(message, self.strings('join', message))

    async def client_ready(self, client, db):
        self.client = client
        self.is_bot = await client.is_bot()
        self.db = db
