from pydub import AudioSegment
from .. import loader, utils
import io
import os
def register(cb):
	cb(AudioShakalMod())
class AudioShakalMod(loader.Module):
	"""АудиоШакал"""
	strings = {'name': 'АудиоШакал'}
	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []
	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()
	async def fvcmd(self, message):
		"""<b>.fv <reply to voice/mp3/ogg/oga> [шакал_lvl(не обязательно, по умолчанию 100 (от 10 до 100))]
		    Сшакалить войс/mp3/ogg/oga</b>
		"""
		reply = await message.get_reply_message()
		lvl = 0
		if not reply:
			await message.edit("<b>Ответь на аудио стоны, еблан</b>")
			return
		if utils.get_args_raw(message):
			ar = utils.get_args_raw(message)
			try:
				int(ar)
				if int(ar) >= 10 and int(ar) <= 100:
					lvl = int(ar)
				else:
					await message.edit("<b>Укажите уровень долбоебизма от 10 до 100!</b>")
					return
			except Exception as exx:
				await message.edit("<b>Неверный аргумент(ты уебок кста)!</b>")
				return
		else:
			lvl = 100
		await message.edit("<b>Ебем Стасяна... (прости Стасян)</b>\n                     Прощаю (с) Стасян")
		sa = False
		m = io.BytesIO()
		fname = await message.client.download_media(message=reply.media)
		if(fname.endswith(".oga") or fname.endswith(".ogg")):
			audio = AudioSegment.from_file(fname, "ogg")
		elif(fname.endswith(".mp3")):
			sa = True
			audio = AudioSegment.from_file(fname, "mp3")
		else:
			await message.edit("<b>Ты еблан? Я(.fv) не поддерживаю этот ёбаный файл! Только voice/mp3/ogg/oga!</b>")
			os.remove(fname)
			return
		audio = audio + lvl
		if(sa):
			m.name = "Ты Шакал.mp3"
			audio.export(m, format="mp3")
		else:
			m.name="voice.ogg"
			audio.split_to_mono()
			audio.export(m, format="ogg", codec="libopus", bitrate="64k")
		m.seek(0)
		if(sa):
			await message.client.send_file(message.to_id, m, reply_to=reply.id)
		else:
			await message.client.send_file(message.to_id, m, reply_to=reply.id, voice_note=True)
		await message.delete()
		os.remove(fname)
