from .. import loader, utils
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import io
from textwrap import wrap


def register(cb):
	cb(ZapomniZabudSoglMod())
	
class ZapomniZabudSoglMod(loader.Module):
	"""Запомните;забудьте твари, согласен."""
	strings = {'name': 'Запомните;забудьте твари, согласен'}
	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []
	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()
		
	async def zapcmd(self, message):
		""".zap <текст или реплай>"""
		
		ufr = requests.get("https://fl1yd.ml/modules/stuff/font.ttf")
		f = ufr.content
		
		reply = await message.get_reply_message()
		txet = utils.get_args_raw(message)
		if not txet:
			if not reply:
				await message.edit("text?")
			else:
				txt = reply.raw_text
		else:
			txt = utils.get_args_raw(message)


		await message.edit("<b>Извиняюсь...</b>")
		pic = requests.get("https://fl1yd.ml/modules/stuff/man.jpg")
		pic.raw.decode_content = True
		img = Image.open(io.BytesIO(pic.content)).convert("RGB")
		black = Image.new("RGBA", img.size, (0, 0, 0, 100))
		img.paste(black, (0, 0), black)

		W, H = img.size
		txt = txt.replace("\n", "𓃐")
		text = "\n".join(wrap(txt, 40))
		t = "Запомните твари:\n" +text
		t = t.replace("𓃐","\n")
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype(io.BytesIO(f), 32, encoding='UTF-8')
		w, h = draw.multiline_textsize(t, font=font)
		imtext = Image.new("RGBA", (w+20, h+20), (0, 0,0,0))
		draw = ImageDraw.Draw(imtext)
		draw.multiline_text((10, 10),t,(255,255,255),font=font, align='center')
		imtext.thumbnail((W, H))
		w, h = imtext.size
		img.paste(imtext, ((W-w)//2,(H-h)//2), imtext)
		out = io.BytesIO()
		out.name = "out.jpg"
		img.save(out)
		out.seek(0)
		await message.client.send_file(message.to_id, out, reply_to=reply)
		await message.delete()


	async def zabcmd(self, message):
		""".zab <текст или реплай>"""

		ufr = requests.get("https://fl1yd.ml/modules/stuff/font.ttf")
		f = ufr.content

		reply = await message.get_reply_message()
		txet = utils.get_args_raw(message)
		if not txet:
			if not reply:
				await message.edit("text?")
			else:
				txt = reply.raw_text
		else:
			txt = utils.get_args_raw(message)

		await message.edit("<b>Извиняюсь...</b>")
		pic = requests.get("https://fl1yd.ml/modules/stuff/man.jpg")
		pic.raw.decode_content = True
		img = Image.open(io.BytesIO(pic.content)).convert("RGB")
		black = Image.new("RGBA", img.size, (0, 0, 0, 100))
		img.paste(black, (0, 0), black)

		W, H = img.size
		txt = txt.replace("\n", "𓃐")
		text = "\n".join(wrap(txt, 40))
		t = "Забудьте твари:\n" + text
		t = t.replace("𓃐", "\n")
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype(io.BytesIO(f), 32, encoding='UTF-8')
		w, h = draw.multiline_textsize(t, font=font)
		imtext = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
		draw = ImageDraw.Draw(imtext)
		draw.multiline_text((10, 10), t, (255, 255, 255), font=font, align='center')
		imtext.thumbnail((W, H))
		w, h = imtext.size
		img.paste(imtext, ((W - w) // 2, (H - h) // 2), imtext)
		out = io.BytesIO()
		out.name = "out.jpg"
		img.save(out)
		out.seek(0)
		await message.client.send_file(message.to_id, out, reply_to=reply)
		await message.delete()


	async def soglcmd(self, message):
		""".sogl <текст или реплай>"""

		ufr = requests.get("https://fl1yd.ml/modules/stuff/font.ttf")
		f = ufr.content

		reply = await message.get_reply_message()
		txet = utils.get_args_raw(message)
		if not txet:
			if not reply:
				await message.edit("text?")
			else:
				txt = reply.raw_text
		else:
			txt = utils.get_args_raw(message)

		await message.edit("<b>Извиняюсь...</b>")
		pic = requests.get("https://fl1yd.ml/modules/stuff/shrek.jpg")
		pic.raw.decode_content = True
		img = Image.open(io.BytesIO(pic.content)).convert("RGB")
		black = Image.new("RGBA", img.size, (0, 0, 0, 100))
		img.paste(black, (0, 0), black)

		W, H = img.size
		txt = txt.replace("\n", "𓃐")
		text = "\n".join(wrap(txt, 40))
		t = "Согласен, " + text
		t = t.replace("𓃐", "\n")
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype(io.BytesIO(f), 28, encoding='UTF-8')
		w, h = draw.multiline_textsize(t, font=font)
		imtext = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
		draw = ImageDraw.Draw(imtext)
		draw.multiline_text((10, 10), t, (255, 255, 255), font=font, align='center')
		imtext.thumbnail((W, H))
		w, h = imtext.size
		img.paste(imtext, ((W - w) // 2, (H - h) // 2), imtext)
		out = io.BytesIO()
		out.name = "out.jpg"
		img.save(out)
		out.seek(0)
		await message.client.send_file(message.to_id, out, reply_to=reply)
		await message.delete()