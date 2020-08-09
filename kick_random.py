from .. import loader
from asyncio import sleep
import random


def register(cb):
	cb(KickRandomMod())

class KickRandomMod(loader.Module):
	"""Кик рандом"""
	strings = {'name': 'KickRandom'}

	async def kickrandcmd(self, event):
		"""Используй .kickrand, чтобы кикнуть случайного пользователя (может кикнуть вас)."""
		user = random.choice([i for i in await event.client.get_participants(event.to_id)])

		await event.edit('<b>Кому-то сейчас не повезёт...</b>')
		await sleep(3)

		# Попытка кика...
		try:
			await event.client.kick_participant(event.chat_id, user.id)
			await sleep(0.5)
		except:
			await event.edit('<b>У меня нет достаточных прав :с</b>')
			return

		# Кто кикнут.
		name = str(user.first_name)
		name += " "+user.last_name if user.last_name else ''
		await event.edit(f"Рандом выбрал <a href=\"tg://user?id={user.id}\">{user.first_name}</a>, и он кикнут!")
