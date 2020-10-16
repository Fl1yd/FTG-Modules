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
    
    async def impscmd(self, message):
        """Используй: .imps <@ или текст или реплай>."""
        try:
            await message.edit("Минуточку...")
            font = requests.get("https://github.com/Fl1yd/FTG-modules/blob/master/stuff/font2.ttf?raw=true").content
            backgrouds = ["https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor2.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor3.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor4.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor5.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor6.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor7.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor8.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor9.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor10.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor11.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor12.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor13.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor14.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor15.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor16.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor17.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor18.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor19.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor20.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor21.png",
                          "https://raw.githubusercontent.com/Fl1yd/FTG-modules/master/stuff/impostor22.png"]
            background = requests.get(f"{choice(backgrouds)}").content
            reply = await message.get_reply_message()
            args = utils.get_args_raw(message)
            imps = ['wasn`t the impostor', 'was the impostor']
            if not args and not reply:
                user = await message.client.get_me()
                text = (f"{user.first_name} {choice(imps)}\n"
                        f"{randint(1, 2)} impostor(s) remain.")
            if reply:
                user = await utils.get_user(await message.get_reply_message())
                text = (f"{user.first_name} {choice(imps)}\n"
                        f"{randint(1, 2)} impostor(s) remain.")
            if args:
                user = await message.client.get_entity(args)
                text = (f"{user.first_name} {choice(imps)}\n"
                        f"{randint(1, 2)} impostor(s) remain.")
            font = io.BytesIO(font)
            font = ImageFont.truetype(font, 30)
            image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            w, h = draw.multiline_textsize(text=text, font=font)
            image = Image.open(io.BytesIO(background))
            x, y = image.size
            draw = ImageDraw.Draw(image)
            draw.multiline_text(((x-w)//2, (y-h)//2), text=text, font=font, fill="white", align="center")
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