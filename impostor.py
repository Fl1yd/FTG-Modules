import io
import requests
from .. import loader, utils
from random import choice, randint
from PIL import Image, ImageDraw, ImageFont


def register(cb):
    cb(ImpMod())

class ImpMod(loader.Module):
    """Among Us"""
    strings = {'name': 'Impostor?'}

    async def impcmd(self, message):
        """Используй: .imp <@ или текст или реплай>."""
        try:
            background = requests.get(f"https://fl1yd.ml/modules/stuff/impostor{randint(1,22)}.png").content
            font = requests.get("https://fl1yd.ml/modules/stuff/font2.ttf").content
            await message.edit("Минуточку...")
            reply = await message.get_reply_message()
            args = utils.get_args_raw(message)
            imps = ['wasn`t the impostor', 'was the impostor']
            if not args and not reply:
                user = await message.client.get_me()
                text = (f"{user.first_name} {choice(imps)}.\n"
                        f"{randint(1, 2)} impostor(s) remain.")
            if reply:
                user = await utils.get_user(await message.get_reply_message())
                text = (f"{user.first_name} {choice(imps)}.\n"
                        f"{randint(1, 2)} impostor(s) remain.")
            if args:
                user = await message.client.get_entity(args)
                text = (f"{user.first_name} {choice(imps)}.\n"
                        f"{randint(1, 2)} impostor(s) remain.")
            font = io.BytesIO(font)
            font = ImageFont.truetype(font, 30)
            image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            w, h = draw.multiline_textsize(text=text, font=font)
            image = Image.open(io.BytesIO(background))
            x, y = image.size
            draw = ImageDraw.Draw(image)
            draw.multiline_text(((x - w) // 2, (y - h) // 2), text=text, font=font, fill="white", align="center")
            output = io.BytesIO()
            output.name = "impostor.png"
            image.save(output, "png")
            output.seek(0)
            await message.client.send_file(message.to_id, output, reply_to=reply)
            await message.delete()
        except:
            text = args
            font = io.BytesIO(font)
            font = ImageFont.truetype(font, 30)
            image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            w, h = draw.multiline_textsize(text=text, font=font)
            image = Image.open(io.BytesIO(background))
            x, y = image.size
            draw = ImageDraw.Draw(image)
            draw.multiline_text(((x - w) // 2, (y - h) // 2), text=text, font=font, fill="white", align="center")
            output = io.BytesIO()
            output.name = "impostor.png"
            image.save(output, "png")
            output.seek(0)
            await message.client.send_file(message.to_id, output, reply_to=reply)
            await message.delete()


    async def ruimpcmd(self, message):
        """Используй: .ruimp <@ или текст или реплай>."""
        try:
            background = requests.get(f"https://fl1yd.ml/modules/stuff/impostor{randint(1,22)}.png").content
            font = requests.get("https://fl1yd.ml/modules/stuff/font2.ttf").content
            await message.edit("Минуточку...")
            reply = await message.get_reply_message()
            args = utils.get_args_raw(message)
            imps = ['не был предателем', 'оказался одним из предалатей']
            remain = randint(1, 2)
            if remain == 1:
                if not args and not reply:
                    user = await message.client.get_me()
                    text = (f"{user.first_name} {choice(imps)}.\n"
                            "1 предатель остался.")
                if reply:
                    user = await utils.get_user(await message.get_reply_message())
                    text = (f"{user.first_name} {choice(imps)}.\n"
                            "1 предатель остался.")
                if args:
                    user = await message.client.get_entity(args)
                    text = (f"{user.first_name} {choice(imps)}.\n"
                            "1 предатель остался.")
            else:
                if not args and not reply:
                    user = await message.client.get_me()
                    text = (f"{user.first_name} {choice(imps)}.\n"
                            "2 предателя осталось.")
                if reply:
                    user = await utils.get_user(await message.get_reply_message())
                    text = (f"{user.first_name} {choice(imps)}.\n"
                            "2 предателя осталось.")
                if args:
                    user = await message.client.get_entity(args)
                    text = (f"{user.first_name} {choice(imps)}.\n"
                            "2 предателя осталось.")
            font = io.BytesIO(font)
            font = ImageFont.truetype(font, 30)
            image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            w, h = draw.multiline_textsize(text=text, font=font)
            image = Image.open(io.BytesIO(background))
            x, y = image.size
            draw = ImageDraw.Draw(image)
            draw.multiline_text(((x - w) // 2, (y - h) // 2), text=text, font=font, fill="white", align="center")
            output = io.BytesIO()
            output.name = "impostor.png"
            image.save(output, "png")
            output.seek(0)
            await message.client.send_file(message.to_id, output, reply_to=reply)
            await message.delete()
        except:
            text = args
            font = io.BytesIO(font)
            font = ImageFont.truetype(font, 30)
            image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            w, h = draw.multiline_textsize(text=text, font=font)
            image = Image.open(io.BytesIO(background))
            x, y = image.size
            draw = ImageDraw.Draw(image)
            draw.multiline_text(((x - w) // 2, (y - h) // 2), text=text, font=font, fill="white", align="center")
            output = io.BytesIO()
            output.name = "impostor.png"
            image.save(output, "png")
            output.seek(0)
            await message.client.send_file(message.to_id, output, reply_to=reply)
            await message.delete()