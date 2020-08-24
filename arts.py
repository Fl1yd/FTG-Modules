from .. import loader, utils


def register(cb):
    cb(ArtsMod())


class ArtsMod(loader.Module):
    """Юникод арты"""
    strings = {'name': 'UnicodeArts'}

    async def vjuhcmd(self, message):
        """Используй .vjuh <текст> c:"""
        text = utils.get_args_raw(message)
        if not text:
            await message.edit('<b>Нету текста после команды :c</b>')
            return
        else:
            vjuh = ("<code>.∧＿∧\n"
                    "( ･ω･｡)つ━☆・*。\n"
                    "⊂  ノ    ・゜ .\n"
                    "しーＪ   °。  *´¨)\n"
                    "             .· ´¸.·*´¨) ¸.·*¨)\n"
                    "                     (¸.·´ (¸.·'* ☆\n\n"
                    "Вжух и ты </code>" + """<code>{}</code>""").format(text)
            await message.edit(vjuh)

        if text == "podpiska":
            await message.edit("<code>.∧＿∧\n"
                               "( ･ω･｡)つ━☆・*。\n"
                               "⊂  ノ    ・゜ .\n"
                               "しーＪ   °。  *´¨)\n"
                               "             .· ´¸.·*´¨) ¸.·*¨)\n"
                               "                     (¸.·´ (¸.·'* ☆\n\n"
                               "Вжух и ты подпишешься -></code> @ftgmodulesbyfl1yd")


    async def cowsaycmd(self, message):
        """Используй .cowsay <текст> c:"""
        text = utils.get_args_raw(message)
        if not text:
            await message.edit('<b>Нету текста после команды :c</b>')
            return
        else:
            cowsay = ("<code> "
                      "< {} >\n"
                      "\n"
                      "    \   ^__^\n"
                      "        \  (oo)\_______\n"
                      "        (__)\       )\/\n"
                      "            ||----w||\n"
                      "               ||     ||</code>").format(text)
            await message.edit(cowsay)


    async def padayucmd(self, message):
        """Используй .padayu <текст>; ничего c:"""
        text = utils.get_args_raw(message)
        if not text:
            text = ("ПАДАЮ")
            padayu = ("┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃ <b>{}</b>!\n"
                      "┓┏┓┏┓┃ ＼○／\n"
                      "┛┗┛┗┛┃ /\n"
                      "┓┏┓┏┓┃ノ)\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n").format(text)
            await message.edit(padayu)
        else:
            padayu = ("┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃ <b>{}</b>!\n"
                      "┓┏┓┏┓┃ ＼○／\n"
                      "┛┗┛┗┛┃ /\n"
                      "┓┏┓┏┓┃ノ)\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n"
                      "┓┏┓┏┓┃\n"
                      "┛┗┛┗┛┃\n").format(text)
            await message.edit(padayu)


    async def priletelcmd(self, message):
        """Используй .prilitel <текст>; ничего c:"""
        text = utils.get_args_raw(message)
        if not text:
            text = ("Я ЛЮБЛЮ СОСАТЬ ХУИ, А ТЫ?!")
            prilitel = ("▬▬▬.◙.▬▬▬\n"
                        "  ═▂▄▄▓▄▄▂\n"
                        "◢◤ █▀▀████▄▄▄▄◢◤\n"
                        "█▄ █ █▄ ███▀▀▀▀▀▀▀╬\n"
                        "◥█████◤ прилетел сказать что-то важное...\n"
                        "══╩══╩═\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬☻/ - <b>{}</b>\n"
                        "╬═╬/▌\n"
                        "╬═╬/ \ ").format(text)
            await message.edit(prilitel)
        else:
            prilitel = ("▬▬▬.◙.▬▬▬\n"
                        "  ═▂▄▄▓▄▄▂\n"
                        "◢◤ █▀▀████▄▄▄▄◢◤\n"
                        "█▄ █ █▄ ███▀▀▀▀▀▀▀╬\n"
                        "◥█████◤ прилетел сказать что-то важное...\n"
                        "══╩══╩═\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬\n"
                        "╬═╬☻/ - <b>{}</b>\n"
                        "╬═╬/▌\n"
                        "╬═╬/ \ ").format(text)
            await message.edit(prilitel)


    async def huytebecmd(self, message):
        """Используй .huytebe <текст>; ничего c:"""
        text = utils.get_args_raw(message)
        if not text:
            text = ("ХУЙ ТЕБЕ!")
            huytebe = ("...............▄▄▄▄▄\n"
                       "..............▄▌░░░░▐▄\n"
                       "............▐░░░░░░░▌\n"
                       "....... ▄█▓░░░░░░▓█▄\n"
                       "....▄▀░░▐░░░░░░▌░▒▌\n"
                       ".▐░░░░▐░░░░░░▌░░░▌\n"
                       "▐ ░░░░▐░░░░░░▌░░░▐\n"
                       "▐ ▒░░░ ▐░░░░░░▌░▒▒▐ \n"
                       "▐ ▒░░░░▐░░░░░░▌░▒▐\n"
                       "..▀▄▒▒▒▒▐░░░░░░▌▄▀\n"
                       "........ ▀▀▀ ▐░░░░░░▌\n"
                       ".................▐░░░░░░▌\n"
                       ".................▐░░░░░░▌\n"
                       ".................▐░░░░░░▌\n"
                       ".................▐░░░░░░▌\n"
                       "................▐▄▀▀▀▀▀▄▌\n"
                       "...............▐▒▒▒▒▒▒▒▒▌\n"
                       "...............▐▒▒▒▒▒▒▒▒▌\n"
                       "................▐▒▒▒▒▒▒▒▌\n"
                       "..................▀▌▒▀▒▐▀\n"
                       "\n"
                       "<b>{}</b>").format(text)
            await message.edit(huytebe)
        else:
            huytebe = ("...............▄▄▄▄▄\n"
                       "..............▄▌░░░░▐▄\n"
                       "............▐░░░░░░░▌\n"
                       "....... ▄█▓░░░░░░▓█▄\n"
                       "....▄▀░░▐░░░░░░▌░▒▌\n"
                       ".▐░░░░▐░░░░░░▌░░░▌\n"
                       "▐ ░░░░▐░░░░░░▌░░░▐\n"
                       "▐ ▒░░░ ▐░░░░░░▌░▒▒▐ \n"
                       "▐ ▒░░░░▐░░░░░░▌░▒▐\n"
                       "..▀▄▒▒▒▒▐░░░░░░▌▄▀\n"
                       "........ ▀▀▀ ▐░░░░░░▌\n"
                       ".................▐░░░░░░▌\n"
                       ".................▐░░░░░░▌\n"
                       ".................▐░░░░░░▌\n"
                       ".................▐░░░░░░▌\n"
                       "................▐▄▀▀▀▀▀▄▌\n"
                       "...............▐▒▒▒▒▒▒▒▒▌\n"
                       "...............▐▒▒▒▒▒▒▒▒▌\n"
                       "................▐▒▒▒▒▒▒▒▌\n"
                       "..................▀▌▒▀▒▐▀\n"
                       "\n"
                       "<b>{}</b>").format(text)
            await message.edit(huytebe)


    async def lolcmd(self, message):
        """Используй .lol с:"""
        lol = ("┏━┓┈┈╭━━━━╮┏━┓┈┈\n"
               "┃╱┃┈┈┃╱╭╮╱┃┃╱┃┈┈\n"
               "┃╱┗━┓┃╱┃┃╱┃┃╱┗━┓\n"
               "┃╱╱╱┃┃╱╰╯╱┃┃╱╱╱┃\n"
               "┗━━━┛╰━━━━╯┗━━━┛\n")
        await message.edit(lol)


    async def fuckyoucmd(self, message):
        """Используй .fuckyou с:"""
        fuckyou = ("┏━┳┳┳━┳┳┓\n"
                   "┃━┫┃┃┏┫━┫┏┓\n"
                   "┃┏┫┃┃┗┫┃┃┃┃\n"
                   "┗┛┗━┻━┻┻┛┃┃\n"
                   "┏┳┳━┳┳┳┓┏┫┣┳┓\n"
                   "┣┓┃┃┃┃┣┫┃┏┻┻┫\n"
                   "┃┃┃┃┃┃┃┃┣┻┫┃┃\n"
                   "┗━┻━┻━┻┛┗━━━┛\n")
        await message.edit(fuckyou)


    async def housecmd(self, message):
        """Используй .house с:"""
        house = ("╯▅╰╱▔▔▔▔▔▔▔╲╯╯\n"
                 "▕▕╱╱╱╱╱╱╱╱╱╲╲╭╭\n"
                 "▕▕╱╱╱╱╱╱╱╱┛▂╲╲╭\n"
                 "╱▂▂▂▂▂▂╱╱┏▕╋▏╲╲\n"
                 "▔▏▂┗┓▂▕▔┛▂┏▔▂▕▔\n"
                 "▕▕╋▏▕╋▏▏▕┏▏▕╋▏▏\n"
                 "▕┓▔┗┓▔┏▏▕┗▏ ┓▔┏\n")
        await message.edit(house)


    async def hellocmd(self, message):
        """Используй .hello с:"""
        hello = ("┈┈┏┓┏┳━┳┓┏┓┏━━┓┈\n"
                 "┈┈┃┃┃┃┏┛┃┃┃┃┏┓┃┈\n"
                 "┈┈┃┗┛┃┗┓┃┃┃┃┃┃┃┈\n"
                 "┈┈┃┏┓┃┏┛┃┃┃┃┃┃┃┈\n"
                 "┈┈┃┃┃┃┗┓┗┫┗┫╰╯┃┈\n"
                 "┈┈┗┛┗┻━┻━┻━┻━━┛┈\n")
        await message.edit(hello)


    async def coffeecmd(self, message):
        """Используй .coffee <текст>; ничего с:"""
        text = utils.get_args_raw(message)
        if not text:
            text = ("Это тебе :з")
            coffee = ("─▄▀─▄▀\n"
                      "──▀──▀\n"
                      "█▀▀▀▀▀█▄\n"
                      "█░░░░░█─█\n"
                      "▀▄▄▄▄▄▀▀\n\n"
                      "<b>{}</b>").format(text)
            await message.edit(coffee)
        else:
            coffee = ("─▄▀─▄▀\n"
                      "──▀──▀\n"
                      "█▀▀▀▀▀█▄\n"
                      "█░░░░░█─█\n"
                      "▀▄▄▄▄▄▀▀\n\n"
                      "<b>{}</b>").format(text)
            await message.edit(coffee)


    async def tvcmd(self, message):
        """Используй .TV <текст>; ничего с:"""
        text = utils.get_args_raw(message)
        if not text:
            text = ("ТЕЛЕВИЗОР ГОВОРИТ ЧТО ТЫ ДОЛБОЁБ!")
            tv = ("░▀▄░░▄▀\n"
                  "▄▄▄██▄▄▄▄▄░▀█▀▐░▌\n"
                  "█▒░▒░▒░█▀█░░█░▐░▌\n"
                  "█░▒░▒░▒█▀█░░█░░█\n"
                  "█▄▄▄▄▄▄███══════\n\n"
                  "<b>{}</b>").format(text)
            await message.edit(tv)
        else:
            tv = ("░▀▄░░▄▀\n"
                  "▄▄▄██▄▄▄▄▄░▀█▀▐░▌\n"
                  "█▒░▒░▒░█▀█░░█░▐░▌\n"
                  "█░▒░▒░▒█▀█░░█░░█\n"
                  "█▄▄▄▄▄▄███══════\n\n"
                  "<b>{}</b>").format(text)
            await message.edit(tv)


    async def grencmd(self, message):
        """Используй .gren <текст>; ничего с:"""
        text = utils.get_args_raw(message)
        if not text:
            text = ("ВЗРЫВАЮ ТЕБЯ НАХУЙ!")
            gren = ("─▄▀▀███═◯\n"
                    "▐▌▄▀▀█▀▀▄\n"
                    "█▐▌─────▐▌\n"
                    "█▐█▄───▄█▌\n"
                    "▀─▀██▄██▀\n\n"
                    "<b>{}</b>").format(text)
            await message.edit(gren)
        else:
            gren = ("─▄▀▀███═◯\n"
                    "▐▌▄▀▀█▀▀▄\n"
                    "█▐▌─────▐▌\n"
                    "█▐█▄───▄█▌\n"
                    "▀─▀██▄██▀\n\n"
                    "<b>{}</b>").format(text)
            await message.edit(gren)